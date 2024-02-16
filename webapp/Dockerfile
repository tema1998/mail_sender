FROM python:3.10.8
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /webapp
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY mail_sender/requirements.txt ./
RUN pip install -r requirements.txt
COPY ./mail_sender ./mail_sender


CMD ["python3", "./mail_sender/manage.py", "runserver", "0.0.0.0:8000"]