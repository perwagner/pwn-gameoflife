from flask_restplus import Resource

from . import api


class Status(Resource):
    def get(self):
        return {
            "status": "Up and running"
        }, 200


class DB(Resource):
    def get(self):
        return {
            "db": "Database here"
        }, 200


api.add_resource(Status, '/status')
api.add_resource(DB, '/db')

