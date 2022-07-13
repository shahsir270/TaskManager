from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from task.views import TaskCreateView, TaskUpdateView, TaskStatusUpdateView, TaskListView

urlpatterns = [
    path('create/task/', csrf_exempt(TaskCreateView.as_view())),
    path('', TaskListView.as_view()),
    path('update/<int:pk>/task/', csrf_exempt(TaskUpdateView.as_view())),
    path('status/update/<int:pk>/task/', csrf_exempt(TaskStatusUpdateView.as_view())),
]