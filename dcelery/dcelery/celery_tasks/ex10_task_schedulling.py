from datetime import timedelta
from dcelery.celery_config import app

app.conf.beat_schedule = {
    'task1': {
        'task': 'dcelery.celery_tasks.ex10_task_schedulling.task1',
        'schedule': timedelta(seconds=5),
    },
    'task2': {
        'task': 'dcelery.celery_tasks.ex10_task_schedulling.task2',
        'schedule': timedelta(seconds=10),
    }
}

@app.task(queue="tasks")
def task1():
    print("running task1")

@app.task(queue="tasks")
def task2():
    print("running task2")