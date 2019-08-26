from flask_restful import fields
from blueprint import db

class UserDetail(db.Model):
    __tablename__='user_detail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    province = db.Column(db.String(30), nullable=False)
    telephone = db.Column(db.String(15), nullable=False)
    email =  db.Column(db.String(30), nullable=True)
    photo = db.Column(db.Text, nullable=True)

    response_fields={
        'id':fields.Integer,
        'user_id':fields.Integer,
        'address':fields.String,
        'city':fields.String,
        'province':fields.String,
        'telephone':fields.String,
        'email':fields.String,
        'photo':fields.String,
    }

    transaction_response_fields={
        'id':fields.Integer,
        'address':fields.String,
        'city':fields.String,
        'province':fields.String,
        'telephone':fields.String,
        'email':fields.String,
    }


    def __init__(self, user_id, address, city, province, telephone, email, photo):
        self.user_id=user_id
        self.address=address
        self.city=city
        self.province=province
        self.telephone=telephone
        self.email=email
        self.photo=photo


    def __repr__(self):
        return '<User Detail %r>' %self.id