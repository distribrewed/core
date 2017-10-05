import logging

from celery import Celery, signals
from kombu import Exchange
from kombu.common import Broadcast

from distribrewed_core import tasks, settings
from distribrewed_core.routes import master_route, worker_route, all_workers_route, route_task

log = logging.getLogger(__name__)

queue = Celery('distribrewed_queue')

# Broker url
queue.conf.broker_url = 'amqp://{username}:{password}@{host}:{port}/{vhost}'.format(
    host=settings.AMQP_HOST,
    port=settings.AMQP_PORT,
    username=settings.AMQP_USER,
    password=settings.AMQP_PASS,
    vhost=settings.AMQP_VHOST,
)

queue.conf.timezone = 'Atlantic/Reykjavik'

queue.conf.worker_hijack_root_logger = False
queue.conf.task_serializer = 'pickle'
queue.conf.accept_content = ['pickle']

# if os.environ.get('CELERY_LOGGING', 'true').lower() not in ['1', 'true']:
#     logging.getLogger('celery').propagate = False

if settings.CELERY_ALWAYS_EAGER:
    queue.conf.task_always_eager = True  # Run tasks locally
    queue.conf.task_eager_propagates = True  # Always print error stacktrace

# Queue setup
queue.conf.task_default_delivery_mode = 'transient'  # Broker only keeps messages in memory
routes = []

if settings.MASTER_PLUGIN_CLASS is not None:
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
elif settings.WORKER_PLUGIN_CLASS is not None:
    # Assume this is a worker
    worker_id = settings.WORKER_NAME
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


@signals.setup_logging.connect
def setup_logging(*args, **kwargs):
    # If debug
    if settings.DEBUG:
        logging.basicConfig(level=logging.DEBUG, format='%(pathname)s:%(lineno)s: [%(levelname)s] %(message)s')
    else:
        # Standard logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-35s %(levelname)-7s %(message)s')
        logging.getLogger('celery').setLevel(logging.WARNING)


@signals.worker_ready.connect
def load_all_plugins(*args, **kwargs):
    log.info('Loading plugins...')
    m = get_master_plugin()
    w = get_worker_plugin()
    if m:
        log.info('Master plugin: {0}'.format(m.__class__.__name__))
    if w:
        log.info('Worker plugin: {0}'.format(w.__class__.__name__))


@signals.worker_ready.connect
def on_ready(*args, **kwargs):
    m = get_master_plugin()
    w = get_worker_plugin()
    if m:
        tasks.master.call_method_by_name.apply_async(
            args=['_on_ready']
        )
    if w:
        tasks.worker.call_method_by_name.apply_async(
            worker_id=w.name,
            args=['_on_ready']
        )


# noinspection PyProtectedMember
@signals.worker_process_shutdown.connect
def on_shutdown(*args, **kwargs):
    m = get_master_plugin()
    w = get_worker_plugin()
    if m:
        m._on_shutdown()
    if w:
        w._on_shutdown()
