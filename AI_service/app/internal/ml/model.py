from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM, AutoModelForTokenClassification
from transformers import pipeline
from mistralai import Mistral
from ollama import chat
from ollama import ChatResponse
from openai import OpenAI
import io
import app.internal.ml.settings as ml_settings


class Model_NER:
    def __init__(self, nlp: pipeline):
        self.nlp = nlp

    async def init_model(self, model, tokenizer):
        try:
            tokenizer = AutoTokenizer.from_pretrained(tokenizer)
            model = AutoModelForTokenClassification.from_pretrained(model)

            self.nlp = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True)
        except Exception as ex:
            raise ValueError(f"unable to load model: {ex}")

    async def generate(self, text) -> str:
        return self.nlp(text)


class Model_API:
    def __init__(self, api_key, **kwargs):
        super().__init__(**kwargs)
        self.api_key = api_key

    def generate(self, text) -> str:
        model = "mistral-large-latest"

        client = Mistral(api_key=self.api_key)

        response = client.chat.complete(
            model=model,
            messages=[
                {"role": "user", "content": text}
            ]
        )

        return response.choices[0].message.content


def ollama(text) -> str:
    response: ChatResponse = chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': text,
        },
    ])

    return response.message.content


class Model_llama_70B:
    def __init__(self, api_key):
        self.api_key = api_key

    def generate(self, text):
        openai = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepinfra.com/v1/openai",
        )

        stream = False  # or False

        chat_completion = openai.chat.completions.create(
            model="meta-llama/Meta-Llama-3-70B-Instruct",
            messages=[
                {"role": "user", "content": text},
            ],
            stream=stream,
        )

        s = ""
        if stream:
            for event in chat_completion:
                if event.choices[0].finish_reason:
                    print(event.choices[0].finish_reason)
                else:
                    s += str(event.choices[0].delta.content)
        else:
            return chat_completion.choices[0].message.content
        # print()
        # print(chat_completion.usage.prompt_tokens, chat_completion.usage.completion_tokens)


class Model_llama_70B2:
    def __init__(self, api_key):
        self.api_key = api_key

    def generate(self, text):
        openai = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepinfra.com/v1/openai",
        )

        stream = False  # or False

        chat_completion = openai.chat.completions.create(
            model="meta-llama/Meta-Llama-3-70B-Instruct",
            messages=[
                {"role": "user", "content": text},
            ],
            stream=stream,
        )

        s = ""
        if stream:
            for event in chat_completion:
                if event.choices[0].finish_reason:
                    print(event.choices[0].finish_reason)
                else:
                    s += str(event.choices[0].delta.content)
        else:
            return chat_completion.choices[0].message.content


# --- SHORT DESCRIPTION GENERATION ---
_short_desc_pipeline = None

def get_short_desc_pipeline():
    global _short_desc_pipeline
    if _short_desc_pipeline is None:
        tokenizer = AutoTokenizer.from_pretrained(ml_settings.model)
        model = AutoModelForSeq2SeqLM.from_pretrained(ml_settings.model)
        _short_desc_pipeline = pipeline('text2text-generation', model=model, tokenizer=tokenizer)
    return _short_desc_pipeline

def generate_short_description(name: str, category: str) -> str:
    """
    Генерирует очень короткое описание для места по названию и категории.
    """
    prompt = f"Кратко опиши место '{name}' категории '{category}' (1-2 предложения):"
    pipe = get_short_desc_pipeline()
    result = pipe(prompt, max_length=30, num_return_sequences=1, do_sample=True)
    return result[0]['generated_text'].strip()


if __name__ == '__main__':
    print(Model_llama_70B2("18kBsYH2IFrKDsA6sAgNRO4TotwkDa4j").generate("Питание"))