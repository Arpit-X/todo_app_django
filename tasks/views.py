from django.shortcuts import render
from rest_framework import generics
from datetime import datetime

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from tasks.serialisers import TaskSerialiser
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django import forms
from django.urls.base import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin# Create your views here.
# serialser views


class TaskListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = Task
    context_object_name = 'dataSet'
    template_name = 'user_task_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView,self).get_context_data(**kwargs)
        tasks = list(Task.objects.all().filter(user=self.request.user))
        context.update({
            'title':"Task List",
            'user_permission':self.request.user.get_all_permissions(),
            'dataSet':tasks,
        })
        return context

class AddTask(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['id','user','time_created']

class AddTaskView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = Task
    form_class = AddTask
    template_name = "add_task.html"

    def post(self,request,*args,**kwargs):
        task_form = AddTask(request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.user = request.user
            task.time_created = datetime.now()
            task.save()
            return redirect('tasks:show_user_tasks')
        else:
            return redirect('tasks:add_task')


class UpdateTask(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = '/login/'
    model = Task
    form_class = AddTask
    template_name = 'add_task.html'
    success_url = reverse_lazy('tasks:show_user_tasks')

    def has_permission(self):
        task_key = self.kwargs['pk']
        try:
            task_object = Task.objects.get(id=task_key)
        except Exception as e:
            return False
        return  task_details.user == self.request.user

class DeleteTask(DeleteView):
    model = Task
    template_name = "delete_task.html"
    success_url = reverse_lazy('tasks:show_user_tasks')

class TaskListAPIView(LoginRequiredMixin,generics.ListCreateAPIView):
    login_url = '/login/'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    login_url = '/login/'

    serializer_class = TaskSerialiser
    authentication_classes = {SessionAuthentication, BasicAuthentication}
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def has_permission(self):
        task_key=self.kwargs['pk']
        try:
            task_object = Task.objects.get(id=task_key)
        except Exception as e:
            return False
        return task_object.user == self.request.user