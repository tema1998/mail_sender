import json
from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View
from django import http

from .models import EmailHistory, TaskHistory, PeriodicTask, EmailData, TaskCore, User
from .forms import SendEmailForm, CreateTaskForm, SigninForm, SignupForm
from .tasks import send_email_celery


class Index(View):
    """
    Sitemap view of the Mail sender.
    """

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        return render(request, "core/index.html")


class SendEmail(LoginRequiredMixin, View):
    """
    View for sending emails.
    """

    login_url = "signin"

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        form = SendEmailForm()
        return render(request, "core/send_email.html", {"form": form})

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        form = SendEmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_email_celery.delay(
                request.user.id, cd["emails_list"], cd["subject"], cd["message"]
            )
            return redirect("history")

        return render(request, "core/send_email.html", {"form": form})


class History(LoginRequiredMixin, View):
    """
    View returning a list of sent emails of the user.
    """

    login_url = "signin"

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        sent_emails = EmailHistory.objects.filter(user=request.user).order_by(
            "-task_result__date_done"
        )
        task_sent_emails = TaskHistory.objects.filter(user=request.user).order_by(
            "-task_result__date_done"
        )
        return render(
            request,
            "core/history.html",
            {
                "sent_emails": sent_emails,
                "task_sent_emails": task_sent_emails,
            },
        )


class CreateTask(LoginRequiredMixin, View):
    """
    View for creating Tasks.
    """

    login_url = "signin"

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        form = CreateTaskForm()
        return render(request, "core/create_task.html", {"form": form})

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            periodic_task_obj = PeriodicTask.objects.create(
                interval=cd["interval"],
                name=cd["name"],
                task="core.tasks.send_email_beat",
                args=json.dumps(
                    [request.user.id, cd["emails_list"], cd["subject"], cd["message"]]
                ),
            )

            email_data = EmailData.objects.create(
                emails=cd["emails_list"], subject=cd["subject"], message=cd["message"]
            )
            TaskCore.objects.create(
                user=request.user, email_data=email_data, task=periodic_task_obj
            )
            return redirect("tasks")

        return render(request, "core/create_task.html", {"form": form})


class Tasks(LoginRequiredMixin, View):
    """
    View returning a list of user Tasks.
    """

    login_url = "signin"

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        tasks = TaskCore.objects.filter(user=request.user).order_by(
            "-task__date_changed"
        )
        return render(request, "core/tasks.html", {"tasks": tasks})


class EnableDisableTask(LoginRequiredMixin, View):
    """
    View for enabling/disabling a Task.
    """

    login_url = "signin"

    def post(self, request: http.HttpRequest) -> http.HttpResponse:
        beat_task = PeriodicTask.objects.get(id=request.POST["beat_task_id"])
        beat_task.enabled = not beat_task.enabled  # Toggle the enabled status
        beat_task.save()
        return redirect(request.META.get("HTTP_REFERER"))


class DeleteTask(LoginRequiredMixin, View):
    """
    View for deleting a Task.
    """

    login_url = "signin"

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        beat_task = PeriodicTask.objects.get(id=request.POST["beat_task_id"])
        core_task = TaskCore.objects.get(task=beat_task)
        with transaction.atomic():
            core_task.delete()
            beat_task.delete()
        return redirect(request.META.get("HTTP_REFERER"))


class Signup(View):
    """
    View for user registration.
    """

    def get(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        if request.user.is_authenticated:
            return redirect("index")
        return render(request, "core/signup.html", {"signup_form": SignupForm()})

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        if request.user.is_authenticated:
            return redirect("index")

        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            new_user = User.objects.create_user(**signup_form.cleaned_data)
            auth.login(request, new_user)
            return redirect("index")

        return render(request, "core/signup.html", {"signup_form": signup_form})


class Signin(View):
    """
    View for user authentication.
    """

    def get(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        if request.user.is_authenticated:
            return redirect("index")
        return render(request, "core/signin.html", {"signin_form": SigninForm()})

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        signin_form = SigninForm(request.POST)
        if signin_form.is_valid():
            user = auth.authenticate(**signin_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect("index")

        messages.error(request, "Invalid username or password")
        return render(request, "core/signin.html", {"signin_form": signin_form})


class Logout(LoginRequiredMixin, View):
    """
    View for logging out the user.
    """

    login_url = "signin"

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        auth.logout(request)
        return redirect("signin")
