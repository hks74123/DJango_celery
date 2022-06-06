from __future__ import absolute_import,unicode_literals
from urllib import request
from celery import Celery
import os
from django.conf import settings
from pytz import timezone
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_celery.settings')

app = Celery('django_celery')

app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace = 'CELERY')

app.conf.beat_schedule = {
    'send-mail-everyday':{
        'task':'offers.tasks.send_dailymail',
        'schedule':crontab(hour=8,minute=0),

    }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self,request!r}')