import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Turbosquid.settings')

app = Celery('Turbosquid')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
