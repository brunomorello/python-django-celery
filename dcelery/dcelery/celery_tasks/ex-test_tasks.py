from dcelery.celery_config import app

@app.task(queue='tasks')
def t1(a, b, message=None):
    time.sleep(5)
    result = a + b
    if message:
        result = f"{message}: {result}"
    return result

@app.task(queue='tasks')
def t2():
    time.sleep(3)
    return

@app.task(queue='tasks')
def t3():
    time.sleep(3)
    return

def test():
    # call task async
    result = t1.apply_async(args=[12,29], kwargs={"message":"The sum is "})
    
    if result.ready():
        print("task is completed")
    else:
        print("task is still running")
        
    if result.successful():
        print("task completed successfully")
    else:
        print("task encountered an error")
        
    try:
        task_result = result.get()
        print("task result: ", task_result)
    except Exception as e:
        print("exception thrown: ", str(e))
        
    exception = result.get(propagate=False)
    if exception:
        print("an exception occurred during task execution: ", str(exception))
        
def test_sync():
    result = t1.apply_async(args=[12,29], kwargs={"message":"The sum is "})
    task_result = result.get()
    print("task is running synchronously")
    print(task_result)
    
def test_async():
    result = t1.apply_async(args=[12,29], kwargs={"message":"The sum is "})
    print("task is running asynchronously")
    print("TaskID: ", result.task_id)

# Example of task rate limit - redis
# app.conf.task_default_rate_limit = '1/m'

# app.conf.broker_transport_options = {
#     'priority_steps': (list(range(10))),
#     'sep': ':',
#     'queue_order_strategy': 'priority'
# }