from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from .model import Transaction
from blueprint import db, app, shop_required
from flask_jwt_extended import jwt_required, get_jwt_claims
import requests, json, datetime
from blueprint.shop.model import Shop
from blueprint.item.model import Item
from blueprint.user.model import User
from blueprint.user_detail.model import UserDetail




bp_transaction = Blueprint('transaction',__name__)
api = Api(bp_transaction)

class TransactionUserResource(Resource):
    def options(self, id=None):
        return {'message' : 'success'}, 200

    @jwt_required
    def get(self,id):
        claim = get_jwt_claims()
        my_id = claim['id']

        qry_trans=Transaction.query.filter_by(id=id).filter_by(user_id=my_id).first()
        if qry_trans is None:
            return {'status' : 'NOT_FOUND', 'message' : 'Transaction not found'}, 404
        else:
            transaction_data=marshal(qry_trans,Transaction.response_fields)

            qry_item=Item.query.get(transaction_data['item_id'])
            item_data=marshal(qry_item,Item.response_fields)

            qry_shop=Shop.query.get(item_data['shop_id'])

            return {'transaction':marshal(qry_trans,Transaction.response_fields),'item':marshal(qry_item,Item.name_response_fields),'shop':marshal(qry_shop,Shop.transaction_response_fields)}, 200, {'Content-Type':'application/json'}




class TransactionUserListResource(Resource):
    def options(self):
        return {'message' : 'success'}, 200


    @jwt_required
    def get(self):
        claim = get_jwt_claims()
        my_id = claim['id']

        parser=reqparse.RequestParser()

        parser.add_argument('p',type=int, location='args',default=1)
        parser.add_argument('rp',type=int, location='args',default=25)
        parser.add_argument('filter_item_id',location='args', help='invalid title value')       
        parser.add_argument('filter_status',location='args', help='invalid title value')        
        parser.add_argument('sort_by_tanggal',location='args', help='invalid sort value',choices=('desc','asc'))
        args = parser.parse_args()

        offset = (args['p']*args['rp'])-args['rp']

        qry=Transaction.query.filter_by(user_id=my_id)
        
        if args['filter_item_id'] is not None:
            qry=qry.filter_by(item_id=args['filter_item_id'])

        if args['filter_status'] is not None:
            qry=qry.filter_by(status=args['filter_status'])

        if args['sort_by_tanggal'] is not None:
            if args['sort_by'] == 'desc':
                qry = qry.order_by(Transaction.tanggal.desc())
            else:
                qry = qry.order_by(Transaction.tanggal)

        result=[]
        for transaction in qry.limit(args['rp']).offset(offset).all():
            transaction_data=marshal(transaction,Transaction.response_fields)

            qry_item=Item.query.get(transaction_data['item_id'])
            item_data=marshal(qry_item,Item.response_fields)

            qry_shop=Shop.query.get(item_data['shop_id'])
            
            result.append({'transaction':marshal(transaction,Transaction.response_fields),'item':marshal(qry_item,Item.name_response_fields),'shop':marshal(qry_shop,Shop.transaction_response_fields)})

        return result, 200, {'Content-Type':'application/json'}



class TransactionShopResource(Resource):
    def options(self, id=None):
        return {'message' : 'success'}, 200


    @jwt_required
    @shop_required
    def get(self,id):
        claim = get_jwt_claims()
        my_id = claim['id']

        qry_shop=Shop.query.filter_by(user_id=my_id).first()
        shop_data=marshal(qry_shop, Shop.response_fields)

        qry_item=Item.query.filter_by(shop_id=shop_data['id']).all()
        
        qry_trans=Transaction.query.get(id)
        
        if qry_item is None or qry_trans is None :
            return {'status' : 'NOT_FOUND', 'message' : 'Transaction not found'}, 404
        else:
            for item in qry_item:
                transaction_data=marshal(qry_trans,Transaction.response_fields)

                item_data=marshal(item,Item.response_fields)

                if transaction_data['item_id'] == item_data['id']:
                    qry_user=User.query.get(my_id)
                    qry_user_detail=UserDetail.query.filter_by(user_id=my_id).first()

                    return {'transaction':marshal(qry_trans,Transaction.response_fields),'item':marshal(item,Item.name_response_fields),'user':marshal(qry_user,User.transaction_response_fields),'user_detail':marshal(qry_user_detail,UserDetail.transaction_response_fields)}, 200, {'Content-Type':'application/json'}
               
            return {'status' : 'NOT_FOUND', 'message' : 'Transaction not found'}, 404


    @jwt_required
    @shop_required
    def put(self,id):
        claim = get_jwt_claims()
        my_id = claim['id']

        qry1=Shop.query.filter_by(user_id=my_id).first()
        my_shop_id=marshal(qry1, Shop.response_fields)['id']

        qry2=Item.query.filter_by(shop_id=my_shop_id)
        
        qry=Transaction.query.filter_by(id=id).filter_by(status='waitpay').first()
        
        if qry2 is None or qry is None :
            return {'status' : 'NOT_FOUND', 'message' : 'Transaction not found'}, 404
        else:
            for i in qry2:
                if marshal(qry,Transaction.response_fields)['item_id'] == marshal(i,Item.response_fields)['id']:
                    qry.status = 'rent'
                    db.session.commit()
                    return marshal(qry,Item.response_fields), 200, {'Content-Type':'application/json'}

            return {'status' : 'NOT_FOUND', 'message' : 'Transaction not found'}, 404
            


    @jwt_required
    @shop_required
    def delete(self,id):
        claim = get_jwt_claims()
        my_id = claim['id']

        qry1=Shop.query.filter_by(user_id=my_id).first()
        my_shop_id=marshal(qry1, Shop.response_fields)['id']

        qry2=Item.query.filter_by(shop_id=my_shop_id)
        
        qry=Transaction.query.filter_by(id=id).first()
        
        if qry2 is None or qry is None :
            return {'status' : 'NOT_FOUND', 'message' : 'Transaction not found'}, 404
        else:
            for i in qry2:
                if marshal(qry,Transaction.response_fields)['item_id'] == marshal(i,Item.response_fields)['id']:
                    my_qty= int(marshal(i, Item.response_fields)['qty']) + int(marshal(qry, Transaction.response_fields)['qty'])

                    i.qty = my_qty
                    db.session.commit()

                    qry.status = 'cancle'
                    db.session.commit()
               
                    return {'message' : 'Transaction has been deleted'}, 200
               
            return {'status' : 'NOT_FOUND', 'message' : 'Transaction not found'}, 404

    
                   



class TransactionShopListResource(Resource):
    def options(self):
        return {'message' : 'success'}, 200


    @jwt_required
    @shop_required
    def get(self):
        claim = get_jwt_claims()
        my_id = claim['id']

        qry_shop=Shop.query.filter_by(user_id=my_id).first()
        shop_data=marshal(qry_shop, Shop.response_fields)

        qry_item=Item.query.filter_by(shop_id=shop_data['id']).all()
        
        result=[]
        for item in qry_item:
            item_data=marshal(item,Item.response_fields)
            qry_trans = Transaction.query.filter_by(item_id=item_data['id'])
            for transaction in qry_trans:
                qry_user=User.query.get(my_id)
                qry_user_detail=UserDetail.query.filter_by(user_id=my_id).first()

                result.append({'transaction':marshal(transaction,Transaction.response_fields),'item':marshal(item,Item.name_response_fields),'user':marshal(qry_user,User.transaction_response_fields),'user_detail':marshal(qry_user_detail,UserDetail.transaction_response_fields)})

           
        if result is None:
            return {'status' : 'NOT_FOUND', 'message' : 'Transaction not found'}, 404
        else:
            return result, 200, {'Content-Type':'application/json'}



class DoneTransactionResource(Resource):
    def options(self, id=None):
        return {'message' : 'success'}, 200


    @jwt_required
    @shop_required
    def put(self,id):
        claim = get_jwt_claims()
        my_id = claim['id']

        qry1=Shop.query.filter_by(user_id=my_id).first()
        my_shop_id=marshal(qry1, Shop.response_fields)['id']

        qry2=Item.query.filter_by(shop_id=my_shop_id)
        
        qry=Transaction.query.filter_by(id=id).filter_by(status='rent').first()
        
        if qry2 is None or qry is None :
            return {'status' : 'NOT_FOUND', 'message' : 'Transaction not found'}, 404
        else:
            for i in qry2:
                if marshal(qry,Transaction.response_fields)['item_id'] == marshal(i,Item.response_fields)['id']:
                    my_qty= int(marshal(i, Item.response_fields)['qty']) + int(marshal(qry, Transaction.response_fields)['qty'])

                    i.qty = my_qty
                    db.session.commit()

                    qry.status = 'done'
                    db.session.commit()

                    return marshal(qry,Item.response_fields), 200, {'Content-Type':'application/json'}
               
            return {'status' : 'NOT_FOUND', 'message' : 'Transaction not found'}, 404

                    


api.add_resource(TransactionUserResource, '/me/<id>')
api.add_resource(TransactionUserListResource, '/me/list')

api.add_resource(TransactionShopResource, '/shop/<id>')
api.add_resource(TransactionShopListResource, '/shop/list')
api.add_resource(DoneTransactionResource, '/shop/done/<id>') 


        