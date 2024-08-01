from celery import Celery

app = Celery('celery_worker')
app.config_from_object('celeryconfig')

@app.task
def add_numbers():
    return