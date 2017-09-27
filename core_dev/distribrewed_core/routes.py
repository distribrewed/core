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
    log.debug('Routing task {0}'.format(name))
    log.debug('args: {}'.format(args))
    log.debug('kwargs: {}'.format(kwargs))
    log.debug('options: {}'.format(options))
    log.debug('task: {}'.format(task))
    log.debug('kw: {}'.format(kw))
    route = {
        'exchange': options.get('exchange'),
        'exchange_type': options.get('exchange_type'),
        'routing_key': options.get('routing_key')
    }
    send_to_all_workers = options.get('all_workers')
    if send_to_all_workers:
        route = all_workers_route()
    elif name.startswith('distribrewed_core.tasks.master') or options.get('routing_key', '') == 'master':
        route = master_route()
    elif name.startswith('distribrewed_core.tasks.worker'):
        wid = options.get('worker_id')
        assert wid is not None, 'When calling worker tasks you should specify worker_id'
        route = worker_route(wid)
    log.debug('Route {0}'.format(route))
    return route
