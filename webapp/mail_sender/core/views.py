from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView

from .models import SingleEmail
from .forms import EmailForm
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