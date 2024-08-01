from celery import Celery

app = Celery('celery_worker')
app.config_from_object('celeryconfig')
app.conf.imports = ('newapp.tasks')
app.autodiscover_tasks()