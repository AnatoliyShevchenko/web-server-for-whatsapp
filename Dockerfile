FROM python:3.12.3-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install libpq-dev -y

RUN python -m venv /venv

ENV PATH="/venv/bin:$PATH"

ENV WEBHOOK_VERIFY_TOKEN=${WEBHOOK_VERIFY_TOKEN}

ENV GRAPH_API_TOKEN=${GRAPH_API_TOKEN}

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .