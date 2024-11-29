from fastapi import APIRouter, UploadFile, File, Form, Request, Response
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
import asyncio
import app.internal.ml.rag_fusion as rag
import app.internal.ml.model as llm
import app.internal.parsing.parser as parser
from pydantic import BaseModel
from dotenv import load_dotenv
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM, AutoModelForTokenClassification
from transformers import pipeline
import numpy as np
import boto3
import os
import io
import json
import time

router = APIRouter(
    prefix="/api/v1"
)

load_dotenv()
api_key = os.getenv('API_MISTRAL')
api_key_openai = os.getenv('API_LLAMA_70B')
api_backend = os.getenv('API_BACKEND')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
S3_URI = os.getenv('S3_HOST')
S3_PORT = os.getenv('S3_PORT')

model_search = SentenceTransformer('sentence-transformers/multi-qa-mpnet-base-dot-v1')

tokenizer = AutoTokenizer.from_pretrained("Babelscape/wikineural-multilingual-ner")
model = AutoModelForTokenClassification.from_pretrained("Babelscape/wikineural-multilingual-ner")
nlp = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True)


@dataclass
class Generate(BaseModel):
    query: str
    model_type: str
    bucket_name: str
    file_names: list


@dataclass
class Search_Location(BaseModel):
    location: str
    weather: list


def load_data(file_names: list, bucket_name: str, query: str) -> list:
    arr_data = []

    for file in file_names:
        # print(S3_URI, S3_ACCESS_KEY, S3_SECRET_KEY)
        # Настройка клиента S3
        s3 = boto3.client(
            service_name="s3",
            endpoint_url=str(S3_URI),  # Замените на ваш endpoint
            aws_access_key_id=str(S3_ACCESS_KEY),  # Замените на ваш Access Key
            aws_secret_access_key=str(S3_SECRET_KEY),  # Замените на ваш Secret Key
            # region_name='us-east-1'  # Замените на ваш регион, если необходимо
        )

        # Кладём что-то в бакет
        # response = s3.get_object(Bucket=bucket_name,
        #                          Key=file[0])  # Замените 'your_bucket_name' на имя вашего бакета
        # file_content = response['Body'].read()
        #
        # array = np.frombuffer(file_content, dtype=np.float32)
        # np.save("emb_temp.npy", array[:768])
        # response2 = s3.get_object(Bucket=bucket_name,
        #                           Key=file[1])  # Замените 'your_bucket_name' на имя вашего бакета
        # file_content2 = response2['Body'].read()
        # print(file_content2)

        s3.download_file(bucket_name, file[0], f"emb_temp_{file[1]}.npy")
        s3.download_file(bucket_name, file[1], f"emb_temp{file[0]}.txt")

        time.sleep(2)

        arr_data += rag.Rag_fusion(docs=open(f"emb_temp{file[0]}.txt", "r", encoding="utf-8"),
                                   doc_emb=np.load(open(f"emb_temp_{file[1]}.npy", "rb"))).score_docs(query=query,
                                                                                                      model_search=model_search)

    return arr_data


@router.post("/generate")
async def generate(data: Generate):
    arr_data = load_data(file_names=data.file_names, bucket_name=data.bucket_name, query=data.query)

    if data.model_type == "mistral":
        return {
            "message": await rag.Rag_fusion(query=data.query).generate_with_arr(model=llm.Model_API(api_key).generate,
                                                                                arr_data=arr_data)}
    elif data.model_type == "llama3-8B":
        return {
            "message": await rag.Rag_fusion(query=data.query).generate_with_arr(model=llm.ollama, arr_data=arr_data)}
    elif data.model_type == "llama3-70B":
        return {"message": await rag.Rag_fusion(query=data.query).generate_with_arr(
            model=llm.Model_llama_70B(api_key=api_key_openai).generate, arr_data=arr_data)}
    else:
        return {"message": await rag.example(model_search, data.query, api_key)}


@router.post("/search_location")
async def generate(data: Search_Location):
    arr_search = await parser.get_text(f"Куда можно сходить в {data.location}")

    arr_loc = []
    for text in arr_search:
        for loc in nlp(text):
            if loc["entity_group"] == "LOC":
                arr_loc.append(loc["word"])

    answer = llm.Model_API(api_key).generate(
        f"Нам известна погода по дням: {"".join([f"{i[0]} - {i[1]},\n" for i in data.weather])}.\n Выбери лучшее место под погоду, в дождливое время закрытое помещение в солнечную более открытое.\nВыведи только в подобном формате: 01.01-Парк Горькова\n02.01-Галерея\n.")
    answer = [arr.split("-") for arr in answer.split('\n')]

    return {"data": answer}
