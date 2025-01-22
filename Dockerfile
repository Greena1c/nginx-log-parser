FROM python:3.12-slim

RUN pip install --no-cache-dir requests

WORKDIR /app
COPY . /app

CMD ["python", "parts.py"]

