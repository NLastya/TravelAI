FROM python:3.12
WORKDIR /site
COPY . .


RUN pip install --upgrade pip & pip install -r requirements.txt
CMD ["uvicorn", "app:create_app", "--host", "0.0.0.0", "--port", "80"]
