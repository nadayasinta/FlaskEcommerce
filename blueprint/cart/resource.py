from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from .model import Cart
from blueprint import db, app, shop_required
from flask_jwt_extended import jwt_required, get_jwt_claims
import requests, json, datetime
from blueprint.user.model import User
from blueprint.transaction.model import Transaction
from blueprint.item.model import Item


bp_cart = Blueprint('cart',__name__)
api = Api(bp_cart)


class CartResource(Resource):
    def options(self, id=None):
        return {'message' : 'success'}, 200

    @jwt_required
    def get(self,id):
        claim = get_jwt_claims()
        my_id = claim['id']

        qry_cart=Cart.query.filter_by(id=id).filter_by(user_id=my_id).filter_by(status=False).first()

        if qry_cart is None:
            return {'status' : 'NOT_FOUND', 'message' : 'Cart not found'}, 404
        else:
            item_cart = marshal(qry_cart,Cart.response_fields)
            qry_item=Item.query.filter_by(id=item_cart['item_id']).filter_by(status=True).first()
            if qry_item is None:
                return {'status' : 'NOT_FOUND', 'message' : 'Item not found'}, 404
            else:
                return {'cart':item_cart,'item':marshal(qry_item,Item.name_response_fields)}, 200, {'Content-Type':'application/json'}
    

    @jwt_required
    def put(self,id):
        claim = get_jwt_claims()
        my_id = claim['id']

        parser = reqparse.RequestParser()
        parser.add_argument('date', location='json', required=True)
        parser.add_argument('duration', location='json', required=True)
        parser.add_argument('qty', location='json', required=True)

        args = parser.parse_args()

        qry=Cart.query.filter_by(id=id).filter_by(user_id=my_id).filter_by(status=False).first()

        if qry is None:
            return {'status' : 'NOT_FOUND', 'message' : 'Cart not found'}, 404
        else:
            item_id = marshal(qry,Cart.response_fields)['item_id']
            qry2=Item.query.filter_by(id=item_id).filter_by(status=True).first()
            if qry2 is None:
                return {'status' : 'NOT_FOUND', 'message' : 'Item not found'}, 404
            else:
                qry.date = args['date']
                qry.duration =  args['duration']
                qry.qty = args['qty']
                qry.price = int(args['qty'])*int(args['duration'])*int(marshal(qry2,Item.response_fields)['price'])
                db.session.commit()
            
                return {'message' : 'succesfully edit item in cart'}, 200


    @jwt_required
    def delete(self,id):
        claim = get_jwt_claims()
        my_id = claim['id']

        qry=Cart.query.filter_by(id=id).filter_by(user_id=my_id).filter_by(status=False).first()

        if qry is None:
            return {'status' : 'NOT_FOUND', 'message' : 'Cart not found'}, 404
        else:
            item_id = marshal(qry,Cart.response_fields)['item_id']
            qry2=Item.query.filter_by(id=item_id).filter_by(status=True).first()
            if qry2 is None:
                return {'status' : 'NOT_FOUND', 'message' : 'Item not found'}, 404
            else:
                db.session.delete(qry)            
                db.session.commit()

                return {'message' : 'Cart has been deleted'}, 200


class CartListResource(Resource):
    def options(self):
        return {'message' : 'success'}, 200

    @jwt_required
    def get(self):
        claim = get_jwt_claims()
        my_id = claim['id']

        parser=reqparse.RequestParser()
        parser.add_argument('p',type=int, location='args',default=1)
        parser.add_argument('rp',type=int, location='args',default=25)
        args = parser.parse_args()

        offset = (args['p']*args['rp'])-args['rp']

        qry_cart=Cart.query.filter_by(user_id=my_id).filter_by(status=False)

        result=[]
        for cart in qry_cart.limit(args['rp']).offset(offset).all():
            cart_data = marshal(cart,Cart.response_fields)
            qry_item=Item.query.filter_by(id=cart_data['item_id']).filter_by(status=True).first()
            # if qry_item is None:
            #     pass
            # else:
            result.append({'cart':cart_data,'item':marshal(qry_item,Item.name_response_fields)})

        return result, 200, {'Content-Type':'application/json'}


class CheckoutResource(Resource):
    def options(self):
        return {'message' : 'success'}, 200

    @jwt_required
    def post(self):
        claim = get_jwt_claims()
        my_id = claim['id']

        qry_cart=Cart.query.filter_by(user_id=my_id).filter_by(status=False).all()

        if qry_cart is None:
            return {'status' : 'NOT_FOUND', 'message' : 'Cart not found'}, 404
        else:
            result=[]
            for cart in qry_cart:
                cart_data = marshal(cart, Cart.response_fields)
                qry_item = Item.query.filter_by(id=cart_data['item_id']).filter_by(status=True).first()
                # if qry_item is None:
                #     pass
                #     # return {'status' : 'NOT_FOUND', 'message' : 'Item not found'}, 404
                # else:
                item_data = marshal(qry_item, Cart.response_fields)
                if int(item_data['qty'])<int(cart_data['qty']):
                    return {'status' : 'NOT_FOUND', 'message' : 'Stok tidak mencukupi'}, 404
                else:
                    cart.status = True
                    db.session.commit()

                    my_qty = int(item_data['qty']) - int(cart_data['qty'])
                    
                    qry_item.qty = my_qty 
                    db.session.commit()

                    new_transaction = Transaction(cart_data['id'], my_id, cart_data['item_id'], cart_data['date'],cart_data['duration'], cart_data['qty'], "waitpay",cart_data['price'])
                        
                    app.logger.debug('DEBUG : %s', new_transaction)
                    
                    db.session.add(new_transaction)
                    db.session.commit()

                    result.append(marshal(new_transaction,Transaction.response_fields))
                        
            return result, 200, {'Content-Type':'application/json'}

api.add_resource(CartResource, '/<id>')
api.add_resource(CartListResource, '/list')
api.add_resource(CheckoutResource, '/checkout')

