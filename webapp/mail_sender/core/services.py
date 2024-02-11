from django.core.mail import send_mail


def send_email(user_email):
    send_mail(
        'String 1',
        'String 2',
        'artemvol1998@gmail.com',
        [user_email],
        fail_silently=False
    )