from dcelery.celery_config import app
from celery import Task
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR,
                    format='%(actime)s %(levelname)s %(message)s')

class CustomTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        if isinstance(exc, ConnectionError):
            logging.error("Connection error occurred - admin notified")
        else:
            print('{0!r} failed: {1!r}'.format(task_id, exc))
            # perform additional error handling if needed
            
app.Task = CustomTask

@app.task(queue='tasks', autoretry_for=(ConnectionError,), default_retry_delay=5, retry_kwargs={'max_retries': 5})
def test_autoretry():
    raise ConnectionError("Connection error occurred...")