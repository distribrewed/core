# noinspection PyShadowingBuiltins
import logging
from collections import OrderedDict

from rest_framework import serializers
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from core_dev.celery import queue
from distribrewed_core.util import run_task_by_name

log = logging.getLogger(__name__)

tasks = [t for t in queue.tasks.keys() if 'celery' not in t]
tasks.sort()


class CeleryTaskObj:
    def __init__(self, task, res):
        self.taskName = task.name
        self.taskId = res.id


# noinspection PyAbstractClass
class CeleryTaskSerializer(serializers.Serializer):
    taskName = serializers.CharField(help_text='Name of task')
    taskId = serializers.CharField(help_text='Id of task')


class TaskListView(GenericAPIView):
    def get(self, request, format=None):
        return Response(OrderedDict([
            ('availableTasks', [reverse('task-run', request=request, args=[t], format=format)for t in tasks])
        ]), status=status.HTTP_200_OK)


# noinspection PyShadowingBuiltins
class TaskRunView(GenericAPIView):
    serializer_class = CeleryTaskSerializer

    # noinspection PyUnusedLocal
    def get(self, request, id, format=None):
        """
        Run task
        ---
        parameters:
        - name: name
          description: Task name
          required: True
          type: string
          paramType: query
        - name: arg
          description: Task argument
          required: false
          type: string
          paramType: query
        """
        if id not in tasks:
            return Response(OrderedDict([
                ('availableTasks', [reverse('task-run', request=request, args=[t], format=format) for t in tasks])
            ]), status=status.HTTP_404_NOT_FOUND)
        arg = ()
        for key in request.QUERY_PARAMS:
            arg += (key,)
        task = run_task_by_name(id, *arg)
        return Response(
            self.get_serializer(CeleryTaskObj(*task), many=False).data)
