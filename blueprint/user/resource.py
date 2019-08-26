from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from .model import User
from blueprint import db, app
from flask_jwt_extended import jwt_required, get_jwt_claims
import requests, json, datetime

bp_user = Blueprint('user',__name__)
api = Api(bp_user)




class SignUpResource(Resource):
    def options(self):
        return {'message' : 'success'}, 200

    def post(self):
        parser=reqparse.RequestParser()

        parser.add_argument('name', location='json', required=True)
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)

        args=parser.parse_args()

        new_user=User(args['name'], args['username'], args['password'], False)

        app.logger.debug('DEBUG : %s', new_user)

        db.session.add(new_user)
        db.session.commit()

        return {'message' : 'Succesfully create new account'}, 200




class UserResource(Resource):
    def options(self):
        return {'message' : 'success'}, 200

        
    @jwt_required
    def get(self):
        claim = get_jwt_claims()
        my_id = claim['id']

        qry=User.query.get(my_id)
        if qry is None:
            return {'status' : 'NOT_FOUND', 'message' : 'User not found'}, 404
        else:
            return marshal(qry,User.response_fields), 200, {'Content-Type':'application/json'}


    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()

        parser.add_argument('name', location='json', required=True)
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)

        args = parser.parse_args()

        claim = get_jwt_claims()
        my_id = claim['id']
        
        qry=User.query.get(my_id)
        
        if qry is None:
            return {'status' : 'NOT_FOUND', 'message' : 'User not found'}, 404
        else:
            qry.name = args['name'] 
            qry.username = args['username']
            qry.password = args['password']
            db.session.commit()

            return marshal(qry,User.response_fields), 200, {'Content-Type':'application/json'}


    # @jwt_required
    # def delete(self):
    #     claim = get_jwt_claims()
    #     my_id = claim['id']

    #     qry=User.query.get(my_id)
    #     if qry is None:
    #         return {'status' : 'NOT_FOUND', 'message' : 'User not found'}, 404
    #     else:
    #         db.session.delete(qry)
    #         db.session.commit()
    #         return {'message' : 'User has been deleted'}, 200



api.add_resource(SignUpResource, '/addnew')
api.add_resource(UserResource, '/me')
