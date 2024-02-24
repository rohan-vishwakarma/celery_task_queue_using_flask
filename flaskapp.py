from flask import Flask, app
from celery import Celery
from celery.result import AsyncResult
from flask_restful import Api, Resource
from Async.tasks import task, task_add_number
from Async.tasks import celery_app

app = Flask(__name__)
api = Api(app)

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




api.add_resource(Main, '/')

if __name__ == '__main__':
    app.run(debug=True)