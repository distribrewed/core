import logging
import os

from celery import Celery
from kombu import Exchange
from kombu.common import Broadcast

from distribrewed_core.routes import master_route, worker_route, all_workers_route, route_task

log = logging.getLogger(__name__)

queue = Celery('distribrewed_queue')

# Broker url
queue.conf.broker_url = 'amqp://{username}:{password}@{host}:{port}/{vhost}'.format(
    host=os.environ.get('AMQP_HOST', 'rabbitmq'),
    port=os.environ.get('AMQP_PORT', '5672'),
    username=os.environ.get('AMQP_USER', 'distribrewed'),
    password=os.environ.get('AMQP_PASS', 'secretpass'),
    vhost=os.environ.get('AMQP_VHOST', 'celery.distribrewed'),
)

queue.conf.timezone = 'Atlantic/Reykjavik'

queue.conf.worker_hijack_root_logger = False

if os.environ.get('CELERY_LOGGING', 'false').lower() not in ['1', 'true']:
    logging.getLogger('celery').propagate = False

if os.environ.get('CELERY_ALWAYS_EAGER', 'false').lower() in ['1', 'true']:
    queue.conf.task_always_eager = True  # Run tasks locally
    queue.conf.task_eager_propagates = True  # Always print error stacktrace

# Queue setup
queue.conf.task_default_delivery_mode = 'transient'  # Broker only keeps messages in memory
routes = []

if os.environ.get('MASTER_PLUGIN_CLASS', None) is not None:
    # Assume this is master
    all_w_route = all_workers_route()
    m_route = master_route()
    queue.conf.task_queues = (
        Broadcast(
            queue=m_route['exchange'],  # Queue name the same as exchange name
            exchange=Exchange(
                name=m_route['exchange'], type=m_route['exchange_type']
            ),
            routing_key=m_route['routing_key']
        ),
    )
elif os.environ.get('WORKER_PLUGIN_CLASS', None):
    # Assume this is a worker
    worker_id = os.environ.get('WORKER_NAME', os.environ.get('HOSTNAME', None))
    w_route = worker_route(worker_id)
    all_w_route = all_workers_route()
    queue.conf.task_queues = (
        Broadcast(
            queue=w_route['exchange'],  # Queue name the same as exchange name
            exchange=Exchange(
                name=w_route['exchange'], type=w_route['exchange_type']
            ),
            routing_key=w_route['routing_key']
        ),
        Broadcast(
            # queue=w_route['exchange'] + 'worker_id',  # TODO: DO THIS PROPERLY BY BINDING EXCHANGE TO QUEUE
            exchange=Exchange(
                name=all_w_route['exchange'], type=all_w_route['exchange_type']
            ),
            routing_key=all_w_route['routing_key']
        ),
    )
else:
    print('No PLUGIN_CLASS provided! Exiting!')
    exit(1)

queue.conf.task_routes = (route_task,)

# noinspection PyUnresolvedReferences
from distribrewed_core.tasks.master import *
# noinspection PyUnresolvedReferences
from distribrewed_core.tasks.worker import *
