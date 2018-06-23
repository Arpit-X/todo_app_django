from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView
from rest_framework.compat import authenticate
from rest_framework.urls import logout, login
from django.contrib.auth.models import User


class LogInForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput())
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class LoginFormView(View):

    def get(self, request, *args, **kwargs):
        form = LogInForm()
        return render(
            request,
            template_name='login_form.html',
            context={
                'form': form
            }
        )

    def post(self, request, *args, **kwargs):
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:

                login(request,user)
                return redirect('tasks:show_user_tasks')
            else:
                return redirect('login_form')


class LogOut(View):
    def get(self,request):
        logout(request)
        return redirect('login_form')


class SignUpForm(forms.Form):
    first_name = forms.CharField(required=True, widget=forms.TextInput())
    last_name = forms.CharField(required=True, widget=forms.TextInput())
    username = forms.CharField(required=True, widget=forms.TextInput())
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class SignUpFormView(CreateView):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            template_name="signup_form.html",
            context={
                'form': SignUpForm()
            }
        )

    def post(self, request, *args, **kwargd):
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
              User.objects.create_user(**form.cleaned_data)
            except Exception as e:
                pass
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect('tasks:show_user_tasks')
            else:
                return redirect('tasks:login_form')
