
FROM python:3.12-slim

RUN apt-get update && apt-get install -y git

WORKDIR /app

COPY . /app

ENV GIT_USER_NAME="Your Name"
ENV GIT_USER_EMAIL="you@example.com"

CMD git config --global user.name "$GIT_USER_NAME" \
    && git config --global user.email "$GIT_USER_EMAIL" \
    && python parst.py
