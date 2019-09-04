from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from .model import User
from blueprint.user_detail.model import UserDetail
from blueprint.shop.model import Shop
from blueprint.item.model import Item
from blueprint.cart.model import Cart
from blueprint.transaction.model import Transaction

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
        # if qry is None:
        #     return {'status' : 'NOT_FOUND', 'message' : 'User not found'}, 404
        # else:
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
        
        # if qry is None:
        #     return {'status' : 'NOT_FOUND', 'message' : 'User not found'}, 404
        # else:
        qry.name = args['name'] 
        qry.username = args['username']
        qry.password = args['password']
        db.session.commit()

        return marshal(qry,User.response_fields), 200, {'Content-Type':'application/json'}
   
    @jwt_required
    def delete(self):
        claim = get_jwt_claims()
        my_id = claim['id']
        
        qry_user=User.query.get(my_id)
        # if qry_user is None:
        #     return {'status' : 'NOT_FOUND', 'message' : 'User not found'}, 404
        # else:
        qry_user_detail=UserDetail.query.filter_by(user_id=my_id).first()
        if qry_user_detail is not None:
            db.session.delete(qry_user_detail)
            db.session.commit()
        
        qry_shop=Shop.query.filter_by(user_id=my_id).first()
        if qry_shop is not None:
            my_shop_id=marshal(qry_shop,Shop.response_fields)['id']

            qry_item=Item.query.filter_by(shop_id=my_shop_id).all()
            for item in qry_item:
                my_item_id=marshal(item,Item.response_fields)['id']
                qry_cart=Cart.query.filter_by(item_id=my_item_id).all()
                for cart in qry_cart:
                    my_cart_id=marshal(cart,Cart.response_fields)['id']
                    qry_transaction=Transaction.query.filter_by(cart_id=my_cart_id).all()
                    for transaction in qry_transaction:
                        my_item_id=marshal(item,Item.response_fields)['id']
                        db.session.delete(transaction)
                        db.session.commit()
                    db.session.delete(cart)
                    db.session.commit()
                db.session.delete(item)
                db.session.commit()
            db.session.delete(qry_shop)
            db.session.commit()
        db.session.delete(qry_user)
        db.session.commit()
        return {'message' : 'User deleted'}, 200



api.add_resource(SignUpResource, '/addnew')
api.add_resource(UserResource, '/me')
