from flask_restful import fields
from blueprint import db

class Item(db.Model):
    __tablename__='item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=True)   
    detail = db.Column(db.Text, nullable=True)
    photo = db.Column(db.Text, nullable=True)

    response_fields={
        'id':fields.Integer,
        'shop_id':fields.Integer,
        'name':fields.String,
        'qty':fields.Integer,        
        'price':fields.Integer,
        'status':fields.String,
        'category':fields.String,
        'description':fields.String,
        'detail':fields.String,
        'photo':fields.String,
    }

    name_response_fields={
        'id':fields.Integer,
        'name':fields.String,
    }

    def __init__(self, shop_id, name, qty, price, status, category, description, detail, photo):
        self.shop_id=shop_id
        self.name=name
        self.qty=qty        
        self.price=price
        self.status=status
        self.category=category
        self.description=description
        self.detail=detail
        self.photo=photo


    def __repr__(self):
        return '<Item %r>' %self.id