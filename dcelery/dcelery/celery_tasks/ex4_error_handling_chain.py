from celery import chain
from dcelery.celery_config import app

@app.task(queue='tasks')
def add(x, y):
    return x + y

@app.task(queue='tasks')
def multiply(z):
    if z == 0:
        raise ValueError("Error: multiplying by zero")
    return z * 2

@app.task(queue='tasks')
def divide(input):
    return input / 2

def run_task_chain():
    task_chain = chain(add.s(2,(3-3-2)), multiply.s())
    result = task_chain.apply_async()
    result.get()