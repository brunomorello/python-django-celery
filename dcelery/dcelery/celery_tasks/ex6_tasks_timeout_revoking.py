from dcelery.celery_config import app
from time import sleep
import sys

@app.task(queue='tasks', time_limit=10)
def long_running_tasks():
    sleep(6)
    return "Task completed successfully"

@app.task(queue='tasks', bind=True)
def process_task_result(self, result):
    if result is None:
        return "Task was revoked, skipping result processing"
    else:
        return f"Task result: {result}"
    
def execute_task_examples():
    result = long_running_tasks.delay()
    try:
        task_result = result.get(timeout=40)
    except TimeoutError:
        print("Task timed out")
        
    task = long_running_tasks.delay()
    task.revoke(terminate=True)
    
    sleep(3)
    sys.stdout.write(task.status)
    
    if task.status == "REVOKED":
        process_task_result.delay(None) # task was revoked, process accordingly
    else:
        process_task_result.delay(task.result)