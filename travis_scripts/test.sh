#!/bin/bash

set -e

TMP_IMAGE=distribrewed_tmp
DOCKER_DEV_FILE=$(pwd)/docker_dev/Dockerfile

docker build -t ${TMP_IMAGE} -f ${DOCKER_DEV_FILE} .
docker run -it -v $(pwd):/tmp/src -w /tmp/src/core_dev ${TMP_IMAGE} ash -c \
	"set -e && coverage run --source=./distribrewed_core -m unittest discover -s ./tests/ && coverage report &&
	mv .coverage /tmp/src/coverage.txt"

if [[ ${TRAVIS} == "true" ]]; then
   bash <(curl -s https://codecov.io/bash)
fi