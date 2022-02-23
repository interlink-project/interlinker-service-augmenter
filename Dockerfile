FROM python:3.9.10-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y git

RUN pip install -r requirements.txt

COPY . /app

CMD ["python","run.py"]