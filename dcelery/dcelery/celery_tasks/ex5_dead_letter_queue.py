import traceback
from dcelery.celery_config import app
from celery import group

app.conf.task_acks_late = True
app.conf.task_reject_on_worker_lost = True


@app.task(queue='tasks')
def my_task(z):
    try:
        if z == 2:
            raise ValueError("Error wrong number")
    except Exception as e:
        traceback_str = traceback.format_exc()
        task_id = my_task.request.id
        handle_failed_task.apply_async(args=(z, str(e), traceback_str, task_id))
        raise
        
@app.task(queue='dead_letter')
def handle_failed_task(z, exception, traceback_str, task_id):
    print(f"Task failed: task_id={task_id}, z={z}, exception={exception}")
    print(traceback_str)
    return "custom logic to pass"

def run_task_group():
    task_group = group(
        my_task.s(1),
        my_task.s(2),
        my_task.s(3),
    )
    task_group.apply_async()