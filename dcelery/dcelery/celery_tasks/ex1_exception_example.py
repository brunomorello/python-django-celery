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

@app.task(queue='tasks')
def task_with_exception():
    # check failed tasks on Flower admin console
    try:
        raise ConnectionError("Connection error occurred...")
    except ConnectionError:
        logging.error("Connection error occurred...")
        raise ConnectionError("Connection error occurred...")
    except ValueError:
        # Handle Value error (check it on flower admin console)
        logging.error("value error has occurred")
        perform_specific_error_handling()
    except Exception:
        # Handle generic exceptions
        logging.error("a generic exception has occurred...")
        notify_admins()
        perform_fallback()
        
def perform_specific_error_handling():
    # logic to handle it
    pass

def notify_admins():
    # notify admins
    pass

def perform_fallback():
    # fallback action
    pass