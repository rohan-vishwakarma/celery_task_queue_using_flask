from flask import Flask, app, jsonify, request
from celery import Celery
from celery.result import AsyncResult
from flask_restful import Api, Resource
from Async.tasks import celery_app
from Async.tasks import task, task_add_number
from Web.views import DataProcessing
from datetime import timedelta

app = Flask(__name__)
api = Api(app)
app.config['CELERY_BACKEND'] = 'redis://localhost:6379'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'

app.config['CELERYBEAT_SCHEDULE'] ={
    'say-every-5-seconds':{
        'task' : 'return_something',
        'schedule':  20, 
    }
}
app.config['CELERY_TIMEZONE'] = 'UTC'

celery = Celery('worker', backend='redis://localhost:6379', broker='redis://localhost:6379')


class Main(Resource):

    def get(self):
        task.delay()
        return f"Task added with id "
    


@app.route('/addition_task/<int:num1>/<int:num2>', methods=['POST'])
def add_numbers(num1, num2):
    app.logger.info("Invoked method to perform a task")
    r = celery.send_task('Async.tasks.task_add_number',kwargs={'x' : num1, 'y': num2})
    app.logger.info(r.backend)
    return r.id


@app.route('/addition_task/<task_id>', methods=['GET'])
def get_addion_status(task_id):
    status = celery.AsyncResult(task_id)
    return {
        "Status" : status.state
    }


@app.route('/userform', methods=['POST'])
def user_form():
    try:
        username = request.form['username']
        email = request.form['email']
        city = request.form['city']
        status = celery.send_task('Async.tasks.user_form_task',
                kwargs={"username": username, "email": email, "city": city})
        return jsonify({
                "message" : "Form data Submitted Successfully",
                "Task_id" : status.id
            })
    
    
        user_form_task
    except Exception as e:
        app.logger.info(e)








api.add_resource(Main, '/')
api.add_resource(DataProcessing, '/dataprocessing')

if __name__ == '__main__':
    app.app_context()
    app.run(debug=True)