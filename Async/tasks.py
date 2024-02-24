from celery import Celery
from celery.utils.log import get_task_logger

import time

celery_app = Celery('task', backend='redis://localhost:6379', broker='redis://localhost:6379')

logger = get_task_logger(__name__)

@celery_app.task()
def task():
    print("started some work")
    time.sleep(5)
    print("Task complete")



@celery_app.task()
def task_add_number(x, y):
    logger.info('Got Request for the addition')
    time.sleep(30)
    logger.info("Work Finished")
    return x + y
    
