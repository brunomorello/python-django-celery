from datetime import timedelta
from celery.schedules import crontab
from dcelery.celery_config import app

app.conf.beat_schedule = {
    'task1': {
        'task': 'dcelery.celery_tasks.ex12_task_schedule_with_crontab.task1',
        'schedule': crontab(minute='0-59/10', hour='0-13', day_of_week='sat'),
        'kwargs': {'foo':'bar'},
        'args': (1,2),
        'options': {
            'queue': 'tasks',
            'prior': 5,
        }
    },
    'task2': {
        'task': 'dcelery.celery_tasks.ex12_task_schedule_with_crontab.task2',
        'schedule': timedelta(seconds=10),
    }
}

@app.task(queue="tasks")
def task1(val1, val2, **kwargs):
    result = val1 + val2
    print(f"Running crontab for task1 - {result}")

@app.task(queue="tasks")
def task2():
    print("running task2")