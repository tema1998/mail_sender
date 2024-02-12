from django.core.mail import send_mail, send_mass_mail


def send_email(list_of_emails, subject, message):
    send_mail(
        subject,
        message,
        'artemvol1998@gmail.com',
        list_of_emails,
        fail_silently=False
    )
