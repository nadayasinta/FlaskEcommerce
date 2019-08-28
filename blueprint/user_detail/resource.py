from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from .model import UserDetail
from blueprint import db, app
from flask_jwt_extended import jwt_required, get_jwt_claims
import requests, json, datetime

bp_user_detail = Blueprint('user_detail',__name__)
api = Api(bp_user_detail)



class UserDetailResource(Resource):
    def options(self):
        return {'message' : 'success'}, 200

        
    @jwt_required
    def get(self):
        claim = get_jwt_claims()
        my_id = claim['id']

        qry=UserDetail.query.filter_by(user_id=my_id).first()
        if qry is None:
            return {'status' : 'NOT_FOUND', 'message' : 'User detail not found'}, 404
        else:
            return marshal(qry,UserDetail.response_fields), 200, {'Content-Type':'application/json'}

            
    @jwt_required
    def patch(self):
        claim = get_jwt_claims()
        my_id = claim['id']

        parser = reqparse.RequestParser()

        parser.add_argument('address', location='json', required=True)
        parser.add_argument('city', location='json', required=True)
        parser.add_argument('province', location='json', required=True)
        parser.add_argument('telephone', location='json', required=True)
        parser.add_argument('email', location='json', required=False)
        parser.add_argument('photo', location='json', required=False)
        

        args = parser.parse_args()

        qry = UserDetail.query.filter_by(user_id=my_id).first()
        if qry is not None:
            qry.address = args['address']
            qry.city = args['city']
            qry.province = args['province']
            qry.telephone = args['telephone']
            qry.email = args['email']
            qry.photo = args['photo']
            db.session.commit()

            return marshal(qry,UserDetail.response_fields), 200, {'Content-Type':'application/json'}
        else:
            new_user_detail = UserDetail(my_id, args['address'], args['city'], args['province'], args['telephone'], args['email'], args['photo'])

            app.logger.debug('DEBUG : %s', new_user_detail)

            db.session.add(new_user_detail)
            db.session.commit()

            return {'message' : 'succesfully add user detail'}, 200


            

api.add_resource(UserDetailResource, '/me/detail')