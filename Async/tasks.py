import json, time
from celery import Celery
from celery.utils.log import get_task_logger

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

@celery_app.task(serializer='json')
def user_form_task(username, email, city):
    logger.info("Form submittion initiated by worker")
    time.sleep(20)
    id = 1
    data  ={}
    data[id] = {}
    data[id]['username'] = username
    data[id]['email'] = email
    data[id]['city'] = city
    logger.info("Form data submitted successfully")
    return data


    
@celery_app.task(name="scheduler")
def return_something():
    print("something")
    logger.info("Hello! from periodic task")
    return 'something'