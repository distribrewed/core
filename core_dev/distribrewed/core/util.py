import logging

from distribrewed.core.celery import queue

log = logging.getLogger(__name__)


def run_task(task, *args, locally=False):
    log.info('Running task \'{0}\'; Arguments: \'{1}\''.format(task.name, args))
    if locally:
        res = task.apply(args=args)
    else:
        res = task.delay(*args)
    log.info('Task id: \'{0}\''.format(res.id))
    return task, res


def get_task_by_name(name):
    return queue.tasks[name]


def run_task_by_name(name, *args, locally=False):
    return run_task(get_task_by_name(name), *args, locally=locally)
