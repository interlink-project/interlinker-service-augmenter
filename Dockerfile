FROM python:3.9.10-slim-buster

WORKDIR /

COPY requirements.txt .

RUN apt-get update && apt-get install -y git

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python","run.py"]