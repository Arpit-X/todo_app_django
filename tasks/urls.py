from django.urls import path
from .views import *


app_name = "tasks"

urlpatterns = [
    path('add/',AddTaskView.as_view(),name='add_task'),
    path('update/<int:pk>',UpdateTask.as_view(),name='update_task'),
    path('delete/<int:pk>',DeleteTask.as_view(),name="delete_task"),
    path('show/',TaskListView.as_view(),name='show_user_tasks'),
    path('api/<int:pk>',TaskDetailAPIView.as_view()),
]
