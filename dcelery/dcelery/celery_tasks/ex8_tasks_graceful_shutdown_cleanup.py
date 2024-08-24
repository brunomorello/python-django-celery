from dcelery.celery_config import app
from celery.signals import task_failure
import sys

def run_task():
    my_task.apply_async()

@app.task(queue="tasks")
def cleanup_failed_task(task_id, *args, **kwargs):
    sys.stdout.write("CLEAN UP")
    
@app.task(queue="tasks")
def my_task():
    raise ValueError("Task failed")

@task_failure.connect(sender=my_task)
def handle_task_failure(sender=None, task_id=None, **kwargs):
    cleanup_failed_task.delay(task_id)