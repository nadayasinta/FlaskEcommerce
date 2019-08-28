from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprint import db

from ..user.model import User

bp_auth = Blueprint('auth',__name__)
api = Api(bp_auth)


class LogInResource(Resource):
    def options(self):
        return {'message' : 'success'}, 200


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)        
        args = parser.parse_args()
        
        
        qry1 = User.query.filter_by(username=args['username'])
        if qry1.first() is None:
            return {'message': 'Silahkan buat akun'}, 404, {'Content-Type': 'application/json'}
        elif qry1 is not None:
            qry2 = qry1.filter_by(password=args['password']).first()
            if qry2 is None:
                return {'message': 'password salah'}, 404, {'Content-Type': 'application/json'}
            elif qry2 is not None:
                qry_dict = marshal(qry2, User.response_fields)
                token = create_access_token(
                    identity = args['username'], 
                    user_claims={
                        'id': qry_dict['id'],
                        'name': qry_dict['name'],
                        'status':qry_dict['status']
                    }
                )
                return {'token': token}, 200, {'Content-Type': 'application/json'}

class RefreshTokenResources(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        current_claims = get_jwt_claims()
        token = create_access_token(identity=current_user,user_claims=current_claims)
        return {'token':token},200

api.add_resource(LogInResource, '/login')
api.add_resource(RefreshTokenResources, '/refresh')
