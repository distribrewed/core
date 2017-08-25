FROM python:3-alpine

# For psycopg2
RUN apk add --no-cache postgresql-dev g++

ENV TMP_DIR /tmp

RUN mkdir -p ${TMP_DIR}
ADD ./requirements.txt ${TMP_DIR}/requirements.txt
ADD ./docker_dev/requirements.txt ${TMP_DIR}/requirements-dev.txt

RUN pip install -r ${TMP_DIR}/requirements-dev.txt