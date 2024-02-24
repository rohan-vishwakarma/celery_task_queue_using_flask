from flask_restful import Resource


class DataProcessing(Resource):
    def get(self):
        return "get method"
    
    def post(self):
        return "Post method"