docker-compose up -d --build  
docker exec -it django /bin/sh

# create app 
python ./manage.py startapp newapp

# remove all docker containers and images
docker stop ${docker ps -aq} && docker rm ${docker ps -aq} && docker rmi ${docker images -aq}

python manage.py shell
from newapp.tasks import task1, tp2
tp1.delay()

# example of task group 

from celery import group
from newapp.tasks import tp1, tp2, tp3, tp4
task_group = group(tp1.s(), tp2.s(), tp3.s(), tp4.s())
task_group.apply_async()

# example of task chaining

from celery import chain
from newapp.tasks import tp1, tp2, tp3, tp4
task_chain = chain(tp4.s(), tp1.s(), tp2.s(), tp3.s())
task_chain.apply_async()

# install pure-python impl for AMQP (pika)
pip install pika

# test task priorization with rabbitMQ

from dcelery.celery import t1, t2, t3
t2.apply_async(priority=5)
t1.apply_async(priority=6)
t3.apply_async(priority=9)
t2.apply_async(priority=5)
t1.apply_async(priority=6)
t3.apply_async(priority=9)

# inspect task on django

celery inspect active
celery inspect active_queues

# test passing arguments and returning results from celery tasks
from dcelery.celery import t1
result = t1.apply_async(args=[5,10], kwargs={"message":"The sum is "})
result.get()

# testing Flower to monitor workers and tasks
from dcelery.celery import t1, t2, t3, test
t2.apply_async(priority=5)
t1.apply_async(args=[5,10], kwargs={"message":"The sum is "})
t3.apply_async(priority=9)
t2.apply_async(priority=5)
t1.apply_async(args=[5,10], kwargs={"message":"The sum is "})
t3.apply_async(priority=9)
t1.apply_async(args=[5,10], kwargs={"message":"The sum is "})
test()

# testing Custom Class - OOP to handle failure 

from dcelery.celery_tasks.ex1_exception_example import task_with_exception
task_with_exception.delay()

# testing automatic retry for known exceptions

https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying

from dcelery.celery_tasks.ex2_auto_retry import test_autoretry
test_autoretry.delay()

# testing error handling groups

from dcelery.celery_tasks.ex3_error_handling_group import run_tasks
run_tasks()

# testing error handling chain

from dcelery.celery_tasks.ex4_error_handling_chain import run_task_chain
run_task_chain()

in case any task fails during the chain execution, the next task is not being executed

# testing dead leatter queue

from dcelery.celery_tasks.ex5_dead_letter_queue import run_task_group
run_task_group()

# testing task timeouts and revoking

from dcelery.celery_tasks.ex6_tasks_timeout_revoking import execute_task_examples
execute_task_examples()

# testing callback after task failure

from dcelery.celery_tasks.ex7_tasks_callback_after_error import run_task
run_task()

link_error is not being executed by celery task