docker-compose up -d --build  
docker exec -it django /bin/sh

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