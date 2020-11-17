FROM python:3.8.1-alpine

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd  

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY ./requirements /usr/src/app/requirements
RUN pip install -r /usr/src/app/requirements/local.txt

COPY . /usr/src/app
