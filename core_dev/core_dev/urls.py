from django.conf.urls import include, url
from django.contrib import admin

from core_dev.views import TaskRunView, TaskListView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TaskListView.as_view(), name='task-list'),
    url(r'^(?P<id>.*)$', TaskRunView.as_view(), name='task-run'),
]
