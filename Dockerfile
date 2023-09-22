FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /talkylabs
WORKDIR /talkylabs

COPY setup.py .
COPY requirements.txt .
COPY README.md .
COPY talkylabs ./talkylabs
COPY tests ./tests

RUN pip install .
RUN pip install -r tests/requirements.txt
