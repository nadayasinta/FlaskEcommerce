from flask_restful import fields
from blueprint import db

class Transaction(db.Model):
    __tablename__='transaction'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)    
    date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Integer, nullable=False)


    response_fields={
        'id':fields.Integer,
        'cart_id':fields.Integer,
        'user_id':fields.Integer,
        'item_id':fields.Integer,
        'date':fields.String,        
        'duration':fields.Integer,
        'qty':fields.Integer,
        'status':fields.String,
        'price':fields.Integer

    }

    def __init__(self, cart_id, user_id, item_id, date, duration, qty, status, price):
        self.cart_id=cart_id        
        self.user_id=user_id
        self.item_id=item_id        
        self.date=date
        self.duration=duration
        self.qty=qty
        self.status=status
        self.price=price


    def __repr__(self):
        return '<Transaction %r>' %self.id