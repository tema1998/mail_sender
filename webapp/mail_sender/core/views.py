from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView

from .models import *
from .forms import EmailForm, MassEmailForm, CreateTaskForm
from .services import emails_to_json
from .tasks import send_email_celery


# class ContactView(CreateView):
#     model = Contact
#     form_class = ContactForm
#     success_url = '/'
#     template_name = 'core/index.html'
#
#     def form_valid(self, form):
#         form.save()
#         send_email_celery.delay(form.instance.email)
#         return super().form_valid(form)


class Index(View):
    def get(self, request):
        return render(request, 'core/index.html')


class Success(View):
    def get(self, request):
        return render(request, 'core/success.html')


class SendEmail(View):
    def get(self, request):
        form = EmailForm
        return render(request, 'core/send_email.html', {'form': form,})

    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = cd['email']
            subject = cd['subject']
            message = cd['message']

            form = form.save(commit=False)
            form.user = request.user
            form.status = False
            form.save()

            send_email_celery.delay([email,], subject, message)
            return redirect('success')

        return redirect(request.META.get('HTTP_REFERER'), {'form': form})


class SendMassEmail(View):
    def get(self, request):
        form = MassEmailForm
        return render(request, 'core/send_emails.html', {'form': form, })

    def post(self, request):
        form = MassEmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            json_emails = emails_to_json(cd['emails_list'])
            subject = cd['subject']
            message = cd['message']

            MassEmail.objects.create(user=request.user, subject=subject, message=message,
                                     emails=json_emails, number_of_valid_emails=len(json_emails),
                                     status=False)

            send_email_celery.delay(list(json_emails.values()), subject, message)
            return redirect('success')

        return redirect(request.META.get('HTTP_REFERER'), {'form': form})


class History(View):
    def get(self, request):
        user = request.user
        sended_emails = SingleEmail.objects.filter(user=user)
        sended_mass_emails = MassEmail.objects.filter(user=user)
        return render(request, 'core/history.html', {'sended_emails': sended_emails, 'sended_mass_emails': sended_mass_emails, })


class CreateTask(View):
    def get(self, request):
        form = CreateTaskForm
        return render(request, 'core/create_task.html', {'form': form, })

    def post(self, request):
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            day = cd['day']
            hour = cd['hour']
            json_emails = emails_to_json(cd['emails_list'])
            subject = cd['subject']
            message = cd['message']
            print(day)
            print(hour)
            print(json_emails)
            print(subject)
            print(message)

            # MassEmail.objects.create(user=request.user, subject=subject, message=message,
            #                          emails=json_emails, number_of_valid_emails=len(json_emails),
            #                          status=False)
            #
            # send_email_celery.delay(list(json_emails.values()), subject, message)
            # return redirect('success')

        return redirect(request.META.get('HTTP_REFERER'), {'form': form})