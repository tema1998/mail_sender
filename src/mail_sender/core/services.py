import re

from django.core.mail import send_mail

from mail_sender import settings

# Email regex pattern for validation
EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"


def send_email(recipient_list: list, subject: str, message: str) -> None:
    """
    Sends an email using Django's send_mail function.

    :param recipient_list: List of email addresses to send the email to.
    :param subject: Subject of the email.
    :param message: Body of the email.
    """
    send_mail(
        subject,
        message,
        str(settings.EMAIL_HOST_USER),
        recipient_list,
        fail_silently=False,
    )


def validate_email(email: str) -> bool:
    """
    Validates an email address using a regular expression.

    :param email: Email address to validate.
    :return: True if email is valid, otherwise False.
    """
    return re.fullmatch(EMAIL_REGEX, email) is not None


def parse_and_validate_emails(emails_str: str) -> list:
    """
    Parses a string of emails, validates them, and returns a list of valid emails.

    :param emails_str: A comma-separated string of email addresses.
    :return: List of validated email addresses.
    """
    return [
        email.strip().strip("'\"")
        for email in emails_str.split(",")
        if validate_email(email.strip().strip("'\""))
    ]


def validate_emails_and_convert_to_json(emails_str: str) -> dict:
    """
    Converts a string of emails into an enumerated dictionary of validated emails.

    :param emails_str: A comma-separated string of email addresses.
    :return: Dictionary with enumerated valid email addresses.
    """
    validated_emails = parse_and_validate_emails(emails_str)
    return {index: email for index, email in enumerate(validated_emails)}
