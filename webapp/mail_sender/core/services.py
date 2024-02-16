import re

from django.core.mail import send_mail
from mail_sender import settings

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def send_email(list_of_emails, subject, message):
    """
    Extend standard function by setting email from settings.
    """
    send_mail(
        subject,
        message,
        str(settings.EMAIL_HOST_USER),
        list_of_emails,
        fail_silently=False
    )


def validate_email(email):
    """
    Receive email, return True if it has the form email,
    else return False
    """
    if re.fullmatch(regex, email):
        return True
    return False


def parse_and_validate_emails(emails_list):
    """
    Receive list of emails, validate emails,
    returns only validated emails list.
    """
    emails = emails_list.split(',')
    validated_emails = []
    for email in emails:
        s = email.replace("'", "").replace('"', '').replace(' ', '')
        if validate_email(s):
            validated_emails.append(s)
    return validated_emails


def emails_to_json(emails_list):
    """
    Receive list of emails, returns enumerated emails - dict.
    """
    validated_emails = parse_and_validate_emails(emails_list)
    return dict(enumerate(validated_emails))

