#!/bin/bash

set -e

TMP_IMAGE=distribrewed_tmp
DOCKER_DEV_FILE=$(pwd)/docker_dev/Dockerfile

docker build -t ${TMP_IMAGE} -f ${DOCKER_DEV_FILE} .
docker run -it -e CELERY_ALWAYS_EAGER=1 -e TESTING=1 -v $(pwd):/tmp/src -w /tmp/src/core_dev ${TMP_IMAGE} ash -c \
	"set -e && coverage run --source=./distribrewed_core -m unittest discover -s ./tests/ && coverage report && coverage xml &&
	mv coverage.xml /tmp/src/coverage.xml && rm .coverage"

if [[ ${TRAVIS} == "true" ]]; then
   bash <(curl -s https://codecov.io/bash)
fi