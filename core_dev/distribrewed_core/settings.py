import os

# RabbitMQ
AMQP_HOST = os.environ.get('AMQP_HOST', 'rabbitmq')
AMQP_PORT = int(os.environ.get('AMQP_PORT', '5672'))
AMQP_USER = os.environ.get('AMQP_USER', 'distribrewed')
AMQP_PASS = os.environ.get('AMQP_PASS', 'secretpass')
AMQP_VHOST = os.environ.get('AMQP_VHOST', 'celery.distribrewed')

# Celery
CELERY_LOGGING = os.environ.get('CELERY_LOGGING', 'true').lower() not in ['1', 'true']
CELERY_ALWAYS_EAGER = os.environ.get('CELERY_ALWAYS_EAGER', 'false').lower() in ['1', 'true']

# Prometheus
PROMETHEUS_SCRAPE_PORT = int(os.environ.get('PROMETHEUS_SCRAPE_PORT', '9000'))

# Plugins
PLUGIN_DIR = os.environ.get(
    'PLUGIN_DIR',
    os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'base'))
)
MASTER_PLUGIN_CLASS = os.environ.get('MASTER_PLUGIN_CLASS', None)
WORKER_PLUGIN_CLASS = os.environ.get('WORKER_PLUGIN_CLASS', None)
WORKER_NAME = os.environ.get('WORKER_NAME', os.environ.get('HOSTNAME', None))  # TODO: Add random hash too default value
