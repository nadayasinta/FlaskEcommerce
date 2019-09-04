import pytest,json, logging
from flask import Flask, request
from blueprint.user.model import User
from blueprint import app, db
from app import cache

def call_client(request):
    client=app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)


def reset_database():
    db.drop_all()
    db.create_all()

    user = User("unittesting2", "unittesting2", "unittesting2", False)

    db.session.add(user)
    db.session.commit()

def shop_required():
    token = cache.get('test-shop-required')
    token = None
    if token is None:
        data={
            'username' : 'unittesting',
            'password' : 'unittesting'
        }

        req = call_client(request)
        res = req.post('/public/login',data=json.dumps(data),content_type='application/json')

        res_json=json.loads(res.data)

        logging.warning('RESULT :%s', res_json)

        assert res.status_code == 200

        cache.set('test-shop-required', res_json['token'],timeout=60)

        return res_json['token']
    else:
        return token

def user_required():
    token = cache.get('test-shop-required')
    token = None
    if token is None:
        data={
            'username' : 'unittesting2',
            'password' : 'unittesting2'
        }

        req = call_client(request)
        res = req.post('/public/login',data=json.dumps(data),content_type='application/json')

        res_json=json.loads(res.data)

        logging.warning('RESULT :%s', res_json)

        assert res.status_code == 200

        cache.set('test-shop-required', res_json['token'],timeout=60)

        return res_json['token']
    else:
        return token