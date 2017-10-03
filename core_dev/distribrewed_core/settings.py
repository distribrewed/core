import random
from os import environ, path

# Testing
TESTING = environ.get('TESTING', 'false').lower() in ['1', 'true']

# RabbitMQ
AMQP_HOST = environ.get('AMQP_HOST', 'rabbitmq')
AMQP_PORT = int(environ.get('AMQP_PORT', '5672'))
AMQP_USER = environ.get('AMQP_USER', 'distribrewed')
AMQP_PASS = environ.get('AMQP_PASS', 'secretpass')
AMQP_VHOST = environ.get('AMQP_VHOST', 'celery.distribrewed')

# Celery
CELERY_ALWAYS_EAGER = environ.get('CELERY_ALWAYS_EAGER', 'false').lower() in ['1', 'true']

# Prometheus
PROMETHEUS_SCRAPE_PORT = int(environ.get('PROMETHEUS_SCRAPE_PORT', random.randint(30000, 40000)))

# Plugins
PLUGIN_DIR = environ.get(
    'PLUGIN_DIR',
    path.abspath(path.join(path.dirname(path.realpath(__file__)), 'base'))
)
MASTER_PLUGIN_CLASS = environ.get('MASTER_PLUGIN_CLASS', None)
WORKER_PLUGIN_CLASS = environ.get('WORKER_PLUGIN_CLASS', None)

WORKER_NAME = environ.get('WORKER_NAME', environ.get('HOSTNAME', None))  # TODO: Add random hash too default value

if WORKER_NAME.lower() == 'all':
    print("Worker name cannot be 'all'", flush=True)
    exit(-1)

