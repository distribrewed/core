#!/bin/bash

set -e

sed 's/\/base:x64/\/base:arm/g' Dockerfile > Dockerfile.arm
docker run --rm --privileged multiarch/qemu-user-static:register --reset
docker build -t distribrewed/core:arm -f Dockerfile.arm .
docker run -t distribrewed/core:arm python --version

if [[ ${TRAVIS} == "true" ]]; then
    docker login -u="$DOCKER_USER" -p="$DOCKER_PASS"
    docker push distribrewed/core:arm
fi
