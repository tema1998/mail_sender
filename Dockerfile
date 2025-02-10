FROM python:3.10.8
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /s
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./src/mail_sender/requirements.txt ./
RUN pip install -r requirements.txt
COPY ./src/mail_sender ./mail_sender
COPY ./src/start.sh ./
COPY .env ./mail_sender/

CMD ["/bin/bash", "start.sh"]