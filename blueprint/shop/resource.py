from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from .model import Shop
from blueprint import db, app, shop_required
from flask_jwt_extended import jwt_required, get_jwt_claims
import requests, json, datetime
from blueprint.user.model import User
from blueprint.item.model import Item

bp_shop = Blueprint('shop',__name__)
api = Api(bp_shop)

class ShopSignUpResource(Resource):
    def options(self):
        return {'message' : 'success'}, 200

    @jwt_required
    def post(self):
        claim = get_jwt_claims()
        my_id = claim['id']

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('address', location='json', required=True)
        parser.add_argument('city', location='json', required=True)
        parser.add_argument('province', location='json', required=True)
        parser.add_argument('telephone', location='json', required=True)
        parser.add_argument('photo', location='json', required=False)


        args = parser.parse_args()

        qry=Shop.query.filter_by(user_id=my_id).first()

        if qry is not None:
            return {'status' : 'NOT_FOUND', 'message' : 'Shop already exists'}, 404
        else:
            new_shop = Shop(my_id, args['name'], args['address'], args['city'], args['province'], args['telephone'],args['photo'],True)

            app.logger.debug('DEBUG : %s', new_shop)

            db.session.add(new_shop)
            db.session.commit()

            qry2=User.query.get(my_id)
            qry2.status = True
            db.session.commit()

            return marshal(new_shop,Shop.response_fields), 200, {'Content-Type':'application/json'}

class ShopDetailResource(Resource):
    def options(self, id=None):
        return {'message' : 'success'}, 200

    def get(self,id):
        qry=Shop.query.filter_by(id=id).filter_by(status=True).first()
        if qry is None:
            return {'status' : 'NOT_FOUND', 'message' : 'Shop not found'}, 404
        else:
            return marshal(qry,Shop.response_fields), 200, {'Content-Type':'application/json'}


class ShopListResource(Resource):
    def options(self):
        return {'message' : 'success'}, 200

    def get(self):
        parser=reqparse.RequestParser()

        parser.add_argument('p',type=int, location='args',default=1)
        parser.add_argument('rp',type=int, location='args',default=25)
        parser.add_argument('search_by_name',location='args', help='invalid title value')
        parser.add_argument('filter_by_city',location='args', help='invalid title value')       
        parser.add_argument('filter_by_provinsi',location='args', help='invalid title value')        
        parser.add_argument('sort_by',location='args', help='invalid sort value',choices=('desc','asc'))
        args = parser.parse_args()

        offset = (args['p']*args['rp'])-args['rp']

        qry=Shop.query.filter_by(status=True)

        if args['search_by_name'] is not None:
            qry=qry.filter_by(name=args['search_by_name'])
        
        if args['filter_by_city'] is not None:
            qry=qry.filter_by(city=args['filter_by_city'])

        if args['filter_by_provinsi'] is not None:
            qry=qry.filter_by(province=args['filter_by_provinsi'])

        if args['sort_by'] is not None:
            if args['sort_by'] == 'desc':
                qry = qry.order_by(Shop.name.desc())
            else:
                qry = qry.order_by(Shop.name)

        rows=[]
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row,Shop.response_fields))

        return rows, 200, {'Content-Type':'application/json'}


class ShopResource(Resource):
    def options(self):
        return {'message' : 'success'}, 200

    @jwt_required
    @shop_required
    def get(self):
        claim = get_jwt_claims()
        my_id = claim['id']

        qry=Shop.query.filter_by(user_id=my_id).first()
        if qry is None:
            return {'status' : 'NOT_FOUND', 'message' : 'Shop not found'}, 404
        else:
            return marshal(qry,Shop.response_fields), 200, {'Content-Type':'application/json'}
    
    @jwt_required
    @shop_required
    def put(self):
        claim = get_jwt_claims()
        my_id = claim['id']

        parser = reqparse.RequestParser()

        parser.add_argument('name', location='json', required=True)
        parser.add_argument('address', location='json', required=True)
        parser.add_argument('city', location='json', required=True)
        parser.add_argument('province', location='json', required=True)
        parser.add_argument('telephone', location='json', required=True)
        parser.add_argument('photo', location='json', required=False)

        args = parser.parse_args()

        qry=Shop.query.filter_by(user_id=my_id).filter_by(status=True).first()
        if qry is None:
            return {'status' : 'NOT_FOUND', 'message' : 'Shop not found'}, 404
        else:
            qry.user_id = my_id
            qry.name = args['name']
            qry.address = args['address']
            qry.city = args['city']
            qry.province = args['province']
            qry.telephone = args['telephone']
            qry.photo = args['photo']
            db.session.commit()

            return marshal(qry,Shop.response_fields), 200, {'Content-Type':'application/json'}



class ShopActivateResource(Resource):       
    def options(self):
        return {'message' : 'success'}, 200

    @jwt_required
    @shop_required
    def delete(self):
        claim = get_jwt_claims()
        my_id = claim['id']

        qry=Shop.query.filter_by(user_id=my_id).filter_by(status=True).first()
        if qry is None:
            return {'status' : 'NOT_FOUND', 'message' : 'Shop not found'}, 404
        else:
            qry.status = False
            db.session.commit()

            my_shop_id=marshal(qry,Shop.response_fields)['id']
            qry3=Item.query.filter_by(shop_id=my_shop_id).all()
            for item in qry3:
                item.status = False
                db.session.commit()

            return {'message' : 'Shop has been deactivate'}, 200

           
    @jwt_required
    @shop_required
    def put(self):
        claim = get_jwt_claims()
        my_id = claim['id']

        qry=Shop.query.filter_by(user_id=my_id).filter_by(status=False).first()
        if qry is None:
            return {'status' : 'NOT_FOUND', 'message' : 'Shop not found'}, 404
        else:
            qry.status = True
            db.session.commit()

            my_shop_id=marshal(qry,Shop.response_fields)['id']
            qry3=Item.query.filter_by(shop_id=my_shop_id).all()
            for item in qry3:
                item.status = True
                db.session.commit()

            return {'message' : 'Shop has been activate'}, 200



api.add_resource(ShopSignUpResource, '/addnew')
api.add_resource(ShopDetailResource, '/<id>')
api.add_resource(ShopListResource, '/list')
api.add_resource(ShopResource, '/me')
api.add_resource(ShopActivateResource, '/me/activate')



