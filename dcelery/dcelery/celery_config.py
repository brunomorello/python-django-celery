import os
import time
import sentry_sdk

from celery import Celery
from kombu import Exchange, Queue
from sentry_sdk.integrations.celery import CeleryIntegration

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcelery.settings')
app = Celery("dcelery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.task_routes = {'newapp.tasks.task1': {'queue':'queue1'}, 'newapp.tasks.task2': {'queue':'queue2'}}

app.conf.task_queues = [
    Queue('tasks', Exchange('tasks'), routing_key='tasks', queue_arguments={'x-max-priority': 10}),
    Queue('dead_letter', routing_key='dead_letter'),
]

sentry_dsn = "https://cdceead68624988b9313fd7e8ba1493d@o4507817458073600.ingest.de.sentry.io/4507817460039760"

sentry_sdk.init(
    dsn=sentry_dsn,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    # integrations
    integrations=[CeleryIntegration()]
)

app.conf.task_acks_late = True
app.conf.task_queue_max_priority = 10
app.conf.task_default_priority = 5
app.conf.worker_prefetch_multiplier = 1
app.conf.worker_concurrency = 1

base_dir = os.getcwd()
task_folder = os.path.join(base_dir, 'dcelery', 'celery_tasks')

if os.path.exists(task_folder) and os.path.isdir(task_folder):
    task_modules = []
    for filename in os.listdir(task_folder):
        if filename.startswith('ex') and filename.endswith('.py'):
            module_name = f'dcelery.celery_tasks.{filename[:-3]}'
            
            module = __import__(module_name, fromlist=['*'])
            
            for name in dir(module):
                obj = getattr(module, name)
                if callable(obj):
                    task_modules.append(f'{module_name}.{name}')

    app.autodiscover_tasks(task_modules)