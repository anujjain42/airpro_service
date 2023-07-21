import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airpro_service.settings')

celery_app = Celery('airpro_service')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

@celery_app.task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request))
  print('hello world')


celery_app.conf.beat_schedule = {
    'add-every-1-minute': {
        'task': 'read_user_system_data',
        'schedule': 60.0,
    },
    
}
