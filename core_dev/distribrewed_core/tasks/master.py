from __future__ import absolute_import, unicode_literals

import logging

from celery import shared_task

from distribrewed_core.plugin import get_master_plugin
from distribrewed_core.tasks import TOTAL_ERRORS

log = logging.getLogger(__name__)


@shared_task
def call_method_by_name(method, *args):
    m = get_master_plugin()
    log.debug('{0}.{1}{2}'.format(m, method, args))
    try:
        getattr(m, method)(*args)
    except Exception:
        TOTAL_ERRORS.inc()
        raise
