from prometheus_client import Counter

TOTAL_ERRORS = Counter('TOTAL_ERRORS', 'Total errors when processing tasks')