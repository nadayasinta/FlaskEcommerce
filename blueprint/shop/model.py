from flask_restful import fields
from blueprint import db

class Shop(db.Model):
    __tablename__='shop'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    province = db.Column(db.String(30), nullable=False)
    telephone = db.Column(db.String(15), nullable=False)
    photo = db.Column(db.Text, nullable=True)
    status = db.Column(db.Boolean, nullable=False)

    response_fields={
        'id':fields.Integer,
        'user_id':fields.Integer,
        'name':fields.String,        
        'address':fields.String,
        'city':fields.String,
        'province':fields.String,
        'telephone':fields.String,
        'photo':fields.String,
        'status':fields.Boolean,
    }


    transaction_response_fields={
        'id':fields.Integer,
        'name':fields.String,        
        'address':fields.String,
        'city':fields.String,
        'province':fields.String,
        'telephone':fields.String,
    }

    name_response_fields={
        'id':fields.Integer,
        'name':fields.String,   
    }


    def __init__(self, user_id, name, address, city, province, telephone, photo, status):
        self.user_id=user_id
        self.name=name        
        self.address=address
        self.city=city
        self.province=province
        self.telephone=telephone
        self.photo=photo
        self.status=status


    def __repr__(self):
        return '<Shop %r>' %self.id