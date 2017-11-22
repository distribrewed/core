#!/bin/sh

set -e

# Add celery as command if needed
if [ "${1:0:1}" = '-' ]; then
	set -- celery "$@"
fi

# Drop root privileges if we are running celery
# allow the container to be started with `--user`
#if [ "$1" = 'celery' -a "$(id -u)" = '0' ]; then
	#set -- su-exec distribrewed "$@"
#fi

# As argument is not related to celery,
# then assume that user wants to run his own process,
# for example a `bash` shell to explore this image
exec "$@"
