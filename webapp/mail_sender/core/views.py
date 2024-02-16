import json

from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View
from django import http

from .models import *
from .forms import SendEmailForm, CreateTaskForm, SigninForm, SignupForm
from .tasks import send_email_celery


class Index(View):
    """
    Sitemap view of the Mail sender.
    """

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        return render(request, 'core/index.html')


class SendEmail(LoginRequiredMixin, View):
    """
    View for sending of Emails.
    Do a redirection if the email's data is valid,
    else render a template with a Validation error.
    """
    login_url = 'signin'

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        form = SendEmailForm
        return render(request, 'core/send_email.html', {'form': form, })

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        form = SendEmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Emails were converted to JSON in forms
            json_emails_list = cd['emails_list']
            subject = cd['subject']
            message = cd['message']

            send_email_celery.delay(request.user.id, json_emails_list, subject, message)
            return redirect('history')

        return render(request, 'core/send_email.html', {'form': form, })


class History(LoginRequiredMixin, View):
    """
    View returning a list of sent emails of the user.
    """
    login_url = 'signin'

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        sent_emails = EmailHistory.objects.filter(user=request.user).order_by('-task_result__date_done')
        task_sent_emails = TaskHistory.objects.filter(user=request.user).order_by('-task_result__date_done')

        return render(request, 'core/history.html', {'sent_emails': sent_emails,
                                                     'task_sent_emails': task_sent_emails,
                                                     })


class CreateTask(LoginRequiredMixin, View):
    """
    View for creating of Tasks.
    Create a task if the task's data is valid,
    then do a redirection to Tasks page,
    else render a template with a Validation error.
    """
    login_url = 'signin'

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        form = CreateTaskForm
        return render(request, 'core/create_task.html', {'form': form, })

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            json_emails_list = cd['emails_list']
            subject = cd['subject']
            message = cd['message']
            name = cd['name']
            interval = cd['interval']

            periodic_task_obj = PeriodicTask.objects.create(
                interval=interval,
                name=name,
                task="core.tasks.send_email_beat",
                args=json.dumps([request.user.id, json_emails_list, subject, message])
            )

            TaskCore.objects.create(user=request.user, emails=json_emails_list, subject=subject, message=message,
                                    task=periodic_task_obj, number_of_valid_emails=len(json_emails_list))

            return redirect('tasks')
        return render(request, 'core/create_task.html', {'form': form, })


class Tasks(LoginRequiredMixin, View):
    """
    View returning a list of Tasks of the user.
    """
    login_url = 'signin'

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        user = request.user
        tasks = TaskCore.objects.filter(user=user).order_by('-task__date_changed')
        return render(request, 'core/tasks.html', {'tasks': tasks, })


class EnableDisableTask(LoginRequiredMixin, View):
    """
    View for Enabling/Disabling of the Task.
    Enable task if the task was disabled,
    and disable task if the task was enabled
    and do a redirection.
    """

    def post(self, request: http.HttpRequest) -> http.HttpResponse:
        beat_task_id = request.POST['beat_task_id']
        beat_task = PeriodicTask.objects.get(id=beat_task_id)
        if beat_task.enabled:
            beat_task.enabled = 0
        else:
            beat_task.enabled = 1
        beat_task.save()
        return redirect(request.META.get('HTTP_REFERER'))


class DeleteTask(LoginRequiredMixin, View):
    """
    View for Deleting of the Task.
    Delete core_task object and beat_task object,
    using the transaction and do a redirection.
    """
    login_url = 'signin'

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        beat_task_id = request.POST['beat_task_id']
        beat_task = PeriodicTask.objects.get(id=beat_task_id)
        core_task = TaskCore.objects.get(task=beat_task)
        with transaction.atomic():
            core_task.delete()
            beat_task.delete()
        return redirect(request.META.get('HTTP_REFERER'))


class Signup(View):
    """
    View for creating of the User.
    GET: provides a form for registration if
    the user has not been authorized,
    else redirect to Index page.
    POST: Create a User if the form's data is valid,
    then do a redirection to Index page,
    else render a template with a Validation error.
    """

    def get(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        if request.user.is_authenticated:
            return redirect('index')
        else:
            signup_form = SignupForm()
            return render(request, 'core/signup.html', {'signup_form': signup_form})

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        if request.user.is_authenticated:
            return redirect('index')
        else:
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                cd = signup_form.cleaned_data
                username = cd['username']
                email = cd['email']
                password = cd['password']

                new_user = User.objects.create_user(username=username, password=password, email=email)
                auth.login(request, new_user)
                return redirect('index')
            return render(request, 'core/signup.html', {'signup_form': signup_form})


class Signin(View):
    """
    View for authorization.
    GET: provides a form for authorization if
    the user has not been authorized,
    else redirect to Index page.
    POST: Authorizes a User if the form's data is valid,
    then do a redirection to Index page,
    else render a template with a Validation error.
    """

    def get(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        if request.user.is_authenticated:
            return redirect('index')
        else:
            signin_form = SigninForm()
            return render(request, 'core/signin.html', {'signin_form': signin_form})

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        signin_form = SigninForm(request.POST)
        if signin_form.is_valid():
            cd = signin_form.cleaned_data
            user = auth.authenticate(username=cd['username'], password=cd['password'])
            if user:
                auth.login(request, user)
                return redirect('index')
        messages.error(request, f'Invalid username or password')
        return render(request, 'core/signin.html', {'signin_form': signin_form})


class Logout(LoginRequiredMixin, View):
    """
    View allow User to exit from account,
    then redirect to signin page.
    """
    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        auth.logout(request)
        return redirect('signin')
