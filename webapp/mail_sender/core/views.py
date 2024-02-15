import json

from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View

from .models import *
from .forms import SendEmailForm, CreateTaskForm
from .services import emails_to_json
from .tasks import send_email_celery, send_email_beat


class Index(View):
    def get(self, request):
        return render(request, 'core/index.html')


class Success(View):
    def get(self, request):
        return render(request, 'core/success.html')


class SendEmail(View):
    def get(self, request):
        form = SendEmailForm
        return render(request, 'core/send_email.html', {'form': form, })

    def post(self, request):
        form = SendEmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            json_emails_list = emails_to_json(cd['emails_list'])
            subject = cd['subject']
            message = cd['message']

            send_email_celery.delay(request.user.id, json_emails_list, subject, message)
            return redirect('success')

        return redirect(request.META.get('HTTP_REFERER'), {'form': form})


class History(View):
    def get(self, request):
        sent_emails = EmailHistory.objects.filter(user=request.user)
        task_sent_emails = TaskHistory.objects.filter(user=request.user).order_by('-task_result__date_done')

        return render(request, 'core/history.html', {'sent_emails': sent_emails,
                                                     'task_sent_emails': task_sent_emails,
                                                     })


class CreateTask(View):
    def get(self, request):
        form = CreateTaskForm
        return render(request, 'core/create_task.html', {'form': form, })

    def post(self, request):
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            emails_list = cd['emails_list']
            subject = cd['subject']
            message = cd['message']
            name = cd['name']
            interval = cd['interval']
            json_emails_list = emails_to_json(emails_list)

            periodic_task_obj = PeriodicTask.objects.create(
                interval=interval,
                name=name,
                task="core.tasks.send_email_beat",
                args=json.dumps([request.user.id, json_emails_list, subject, message])
                # one_off=True,
            )

            task_core_obj = TaskCore.objects.create(user=request.user, emails=json_emails_list, subject=subject,
                                                    message=message, task=periodic_task_obj,
                                                    number_of_valid_emails=len(json_emails_list))
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect(request.META.get('HTTP_REFERER'), {'form': form})


class Tasks(View):
    def get(self, request):
        user = request.user
        tasks = TaskCore.objects.filter(user=user)
        return render(request, 'core/tasks.html', {'tasks': tasks,})


class EnableDisableTask(View):
    def post(self, request):
        beat_task_id = request.POST['beat_task_id']
        beat_task = PeriodicTask.objects.get(id=beat_task_id)
        if beat_task.enabled:
            beat_task.enabled = 0
        else:
            beat_task.enabled = 1
        beat_task.save()
        return redirect(request.META.get('HTTP_REFERER'))


class DeleteTask(View):
    def post(self, request):
        beat_task_id = request.POST['beat_task_id']
        beat_task = PeriodicTask.objects.get(id=beat_task_id)
        core_task = TaskCore.objects.get(task=beat_task)
        with transaction.atomic():
            core_task.delete()
            beat_task.delete()
        return redirect(request.META.get('HTTP_REFERER'))
