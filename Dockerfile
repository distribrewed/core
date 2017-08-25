FROM distribrewed/base:x64

ENV TMP_DIR=/tmp

COPY . ${TMP_DIR}/core
RUN pip install ${TMP_DIR}/core/ && rm -rf ${TMP_DIR}/*

COPY docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["-A", "distribrewed_core", "worker", "-l", "info", "--concurrency", "1"]