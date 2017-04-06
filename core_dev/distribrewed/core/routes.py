import logging

log = logging.getLogger(__name__)


def master_route():
    return {
        'exchange': 'master',
        'exchange_type': 'topic',
        'routing_key': 'master'
    }


def worker_route(worker_id):
    return {
        'exchange': 'worker.{0}'.format(worker_id),
        'exchange_type': 'topic',
        'routing_key': 'worker.{0}'.format(worker_id)
    }


def all_workers_route():
    return {
        'exchange': 'worker.all',
        'exchange_type': 'topic',
        'routing_key': 'worker.all'
    }


def route_task(name, args, kwargs, options, task=None, **kw):
    route = {}
    send_to_all_workers = options.get('all_workers')
    if send_to_all_workers:
        route = all_workers_route()
    elif name.startswith('distribrewed.core.tasks.master'):
        route = master_route()
    elif name.startswith('distribrewed.core.tasks.worker'):
        wid = options.get('worker_id')
        assert wid is not None, 'When calling worker tasks you should specify worker_id'
        route = worker_route(wid)
    log.debug('Routing: {0}'.format(route))
    return route
