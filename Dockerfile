FROM python:3.9-slim

RUN apt-get update && apt-get install -y libreoffice

WORKDIR /app

ADD . /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000",  "main:app"]
