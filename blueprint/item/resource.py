from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from .model import Item
from blueprint import db, app, shop_required
from flask_jwt_extended import jwt_required, get_jwt_claims
import requests, json, datetime
from blueprint.shop.model import Shop
from blueprint.cart.model import Cart


bp_item = Blueprint('item',__name__)
api = Api(bp_item)


class ItemDetailResource(Resource):
    def options(self, id=None):
        return {'message' : 'success'}, 200

    def get(self,id):
        qry_item=Item.query.filter_by(id=id).filter_by(status=True).first()
        if qry_item is None:
            return {'status' : 'NOT_FOUND', 'message' : 'Item not found'}, 404
        else:
            data_item = marshal(qry_item,Item.response_fields)
            qry_shop = Shop.query.filter_by(id=data_item['shop_id']).first()
            return {'item':data_item,'shop':marshal(qry_shop,Shop.name_response_fields)}, 200, {'Content-Type':'application/json'}


class ItemListResource(Resource):
    def options(self):
        return {'message' : 'success'}, 200

    def get(self):
        parser=reqparse.RequestParser()

        parser.add_argument('p',type=int, location='args',default=1)
        parser.add_argument('rp',type=int, location='args',default=25)
        parser.add_argument('search_by_nama',location='args', help='invalid title value')
        parser.add_argument('filter_by_shop_id',location='args', help='invalid title value')       
        parser.add_argument('filter_by_category',location='args', help='invalid title value')        
        parser.add_argument('sort_by',location='args', help='invalid sort value',choices=('desc','asc'))
        args = parser.parse_args()

        offset = (args['p']*args['rp'])-args['rp']

        qry_item=Item.query.filter_by(status=True)

        if args['search_by_nama'] is not None:
            qry_item=qry_item.filter_by(name=args['search_by_nama'])
        
        if args['filter_by_shop_id'] is not None:
            qry_item=qry_item.filter_by(shop_id=args['filter_by_shop_id'])

        if args['filter_by_category'] is not None:
            qry_item=qry_item.filter_by(category=args['filter_by_category'])

        if args['sort_by'] is not None:
            if args['sort_by'] == 'desc':
                qry_item = qry_item.order_by(Item.name.desc())
            else:
                qry_item = qry_item.order_by(Item.name)

        result=[]
        for item in qry_item.limit(args['rp']).offset(offset).all():
            data_item = marshal(item,Item.response_fields)
            qry_shop = Shop.query.filter_by(id=data_item['shop_id']).first()
            result.append({'item':data_item,'shop':marshal(qry_shop,Shop.name_response_fields)})

        return result, 200, {'Content-Type':'application/json'}

class ItemListAllResource(Resource):
    def options(self):
        return {'message' : 'success'}, 200
   
    @jwt_required        
    @shop_required
    def get(self):
        claim = get_jwt_claims()
        my_id = claim['id']

        qry1=Shop.query.filter_by(user_id=my_id).filter_by(status=True).first()
        if qry1 is None:
            return {'status' : 'NOT_FOUND', 'message' : 'Shop deactive'}, 404
        else:
            my_shop_id=marshal(qry1, Shop.response_fields)['id']


            qry_item=Item.query.filter_by(shop_id=my_shop_id).order_by(Item.status.desc())

            if qry_item is None:
                return {'status' : 'NOT_FOUND', 'message' : 'Item not found'}, 404
            else:
                result=[]
                for item in qry_item.all():
                    data_item = marshal(item,Item.response_fields)
                    qry_shop = Shop.query.filter_by(id=data_item['shop_id']).first()
                    result.append({'item':data_item,'shop':marshal(qry_shop,Shop.name_response_fields)})

                return result, 200, {'Content-Type':'application/json'}


class ItemResource(Resource):
    def options(self, id=None):
        return {'message' : 'success'}, 200


    @jwt_required
    @shop_required
    def post(self):
        claim = get_jwt_claims()
        my_id = claim['id']

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('qty', location='json', required=True)
        parser.add_argument('price', location='json', required=True)
        parser.add_argument('category', location='json', required=True)
        parser.add_argument('description', location='json', required=False)
        parser.add_argument('detail', location='json', required=False)
        parser.add_argument('photo', location='json', required=False)

        args = parser.parse_args()

        
        if int(args['qty']) <1:
            return {'status' : 'NOT_FOUND', 'message' : 'Item qty must >= 1'}, 404

        qry1=Shop.query.filter_by(user_id=my_id).filter_by(status=True).first()
        if qry1 is None:
            return {'status' : 'NOT_FOUND', 'message' : 'Shop deactive'}, 404
        else:
            my_shop_id=marshal(qry1, Shop.response_fields)['id']
                
            # (self, shop_id, name, qty, price, status, category)
            new_item = Item(my_shop_id, args['name'], args['qty'], args['price'], True, args['category'], args['description'], args['detail'],args['photo'] )

            app.logger.debug('DEBUG : %s', new_item)

            db.session.add(new_item)
            db.session.commit()

            return {'message' : 'succesfully add item'}, 200

    
    @jwt_required
    @shop_required
    def put(self,id):
        claim = get_jwt_claims()
        my_id = claim['id']
        
        parser = reqparse.RequestParser()
        
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('qty', location='json', required=True)
        parser.add_argument('price', location='json', required=True)
        parser.add_argument('category', location='json', required=True)
        parser.add_argument('description', location='json', required=False)
        parser.add_argument('detail', location='json', required=False)
        parser.add_argument('photo', location='json', required=False)
        
        args = parser.parse_args()
        
        qry1=Shop.query.filter_by(user_id=my_id).filter_by(status=True).first()
        if qry1 is None:
            return {'status' : 'NOT_FOUND', 'message' : 'Shop deactive'}, 404
        else:
            my_shop_id=marshal(qry1, Shop.response_fields)['id']


            qry=Item.query.filter_by(shop_id=my_shop_id).filter_by(id=id).filter_by(status=True).first()

            if qry is None:
                return {'status' : 'NOT_FOUND', 'message' : 'Item not found'}, 404
            else:
                qry.shop_id = my_shop_id
                qry.name = args['name']
                qry.qty = args['qty']
                qry.price = args['price']
                qry.category = args['category']
                qry.description = args['description']
                qry.detail = args['detail']
                qry.photo = args['photo']
                db.session.commit()
                
                return marshal(qry,Item.response_fields), 200, {'Content-Type':'application/json'}
        
class ItemActivateResource(Resource):
    def options(self, id=None):
        return {'message' : 'success'}, 200

    @jwt_required
    @shop_required
    def delete(self,id):
        claim = get_jwt_claims()
        my_id = claim['id']
        
        qry1=Shop.query.filter_by(user_id=my_id).filter_by(status=True).first()
        if qry1 is None:
            return {'status' : 'NOT_FOUND', 'message' : 'Shop deactive'}, 404
        else:
            my_shop_id=marshal(qry1, Shop.response_fields)['id']

            qry=Item.query.filter_by(shop_id=my_shop_id).filter_by(id=id).filter_by(status=True).first()
            
            if qry is None:
                return {'status' : 'NOT_FOUND', 'message' : 'Item not found'}, 404
            else:
                qry.status = False
                db.session.commit()

                return {'message' : 'Item has been deleted'}, 200


    @jwt_required
    @shop_required
    def put(self,id):
        claim = get_jwt_claims()
        my_id = claim['id']
        
        qry1=Shop.query.filter_by(user_id=my_id).filter_by(status=True).first()
        if qry1 is None:
            return {'status' : 'NOT_FOUND', 'message' : 'Shop deactive'}, 404
        else:
            my_shop_id=marshal(qry1, Shop.response_fields)['id']

            qry=Item.query.filter_by(shop_id=my_shop_id).filter_by(id=id).filter_by(status=False).first()
            
            if qry is None:
                return {'status' : 'NOT_FOUND', 'message' : 'Item not found'}, 404
            else:
                qry.status = True
                db.session.commit()

                return {'message' : 'Item has been activated'}, 200



class NewCartResources(Resource):
    def options(self, id=None):
        return {'message' : 'success'}, 200


    @jwt_required
    def patch(self,id):
        claim = get_jwt_claims()
        my_id = claim['id']

        parser = reqparse.RequestParser()
        parser.add_argument('date', location='json', required=True)
        parser.add_argument('duration', location='json', required=True)
        parser.add_argument('qty', location='json', required=True)

        args = parser.parse_args()

        if int(args['qty']) <1:
            return {'status' : 'NOT_FOUND', 'message' : 'Item qty must >= 1'}, 404
            
        qry=Item.query.filter_by(id=id).filter_by(status=True).first()

        if qry is None:
            return {'status' : 'NOT_FOUND', 'message' : 'Item not found'}, 404
        else:
            qry2 = Cart.query.filter_by(item_id=id).filter_by(user_id=my_id).filter_by(status=False).first()
            req_price = int(marshal(qry, Item.response_fields)['price'])
            if qry2 is not None: 
                req_qty = int(marshal(qry2, Cart.response_fields)['qty'])+int( args['qty'])
                if req_qty > int(marshal(qry, Item.response_fields)['qty']):
                    return {'status' : 'NOT_FOUND', 'message' : 'Stok kurang'}, 404
                else:
                    qry2.date = args['date']
                    qry2.duration =  args['duration']
                    qry2.qty = req_qty
                    qry2.price = (int(args['duration'])*req_qty*req_price)                 
                    db.session.commit()
                
                    return {'message' : 'succesfully add item to cart'}, 200

            elif qry2 is None:
                if int( args['qty']) > int(marshal(qry, Item.response_fields)['qty']):
                    return {'status' : 'NOT_FOUND', 'message' : 'Stok kurang'}, 404
                else:
                    new_price = int(args['duration']) * int(args['qty']) * req_price
                    new_cart = Cart(my_id, id, args['date'], args['duration'], args['qty'], False, new_price)
                    app.logger.debug('DEBUG : %s', new_cart)
                    
                    db.session.add(new_cart)
                    db.session.commit()

                    return {'message' : 'succesfully add item to cart'}, 200

        
        

api.add_resource(ItemDetailResource, '/<id>')
api.add_resource(ItemListResource, '/list')
api.add_resource(ItemListAllResource, '/listall')
api.add_resource(ItemResource, '/me' , '/me/<id>')
api.add_resource(ItemActivateResource, '/me/activate/<id>')
api.add_resource(NewCartResources, '/rent/<id>')



