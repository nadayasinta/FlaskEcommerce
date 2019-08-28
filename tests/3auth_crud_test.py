import json

from . import app, client, cache, shop_required, user_required


class TestAuthEndpoint():
    def test_user_signin(self,client):
        data = {
            "username": "unittesting",
            "password": "unittesting"
        }
        res = client.post('/public/login', data=json.dumps(data),content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_signin_failed(self,client):
        data = {
            "name": "unittesting2",
            "username": "unittesting2"
        }
        res = client.post('/public/login', data=json.dumps(data),content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 400
