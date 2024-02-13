import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mail_sender.settings')

app = Celery('mail_sender')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'send-spam-every-1-minute': {
#         'task': 'core.tasks.send_beat_email',
#         'schedule': crontab(minute='*/1')
#     }
# }