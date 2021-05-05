FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev g++ libopenexr-dev openexr && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "api.py"]