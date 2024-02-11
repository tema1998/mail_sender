from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView

from .models import Contact
from .forms import ContactForm
from .tasks import send_email_celery


# class Index(View):
#     def get(self, request):
#         return render(request, 'core/base.html', {'123': '123', })


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = '/'
    template_name = 'core/index.html'

    def form_valid(self, form):
        form.save()
        send_email_celery.delay(form.instance.email)
        return super().form_valid(form)
