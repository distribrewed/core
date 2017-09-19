#!/bin/sh

sed 's/\/base:x64/\/base:arm/g' Dockerfile > Dockerfile.arm
docker run --rm --privileged multiarch/qemu-user-static:register --reset
docker build -t distribrewed/core:arm -f Dockerfile.arm .
docker run -t distribrewed/core:arm python --version
docker login -u="$DOCKER_USER" -p="$DOCKER_PASS"
docker push distribrewed/core:arm