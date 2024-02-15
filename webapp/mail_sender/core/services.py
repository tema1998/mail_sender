import re

from django.core.mail import send_mail

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def send_email(list_of_emails, subject, message):
    send_mail(
        subject,
        message,
        'artemvol1998@gmail.com',
        list_of_emails,
        fail_silently=False
    )


def validate_email(email):
    if re.fullmatch(regex, email):
        return True
    return False


def parse_and_validate_emails(emails_list):
    emails = emails_list.split(',')
    validated_emails = []
    for email in emails:
        s = email.replace("'", "").replace('"', '').replace(' ', '')
        if validate_email(s):
            validated_emails.append(s)
    return validated_emails


def emails_to_json(emails_list):
    validated_emails = parse_and_validate_emails(emails_list)
    return dict(enumerate(validated_emails))

