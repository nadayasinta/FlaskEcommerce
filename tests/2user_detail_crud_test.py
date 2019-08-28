import json

from . import app, client, cache, shop_required, user_required


class TestUserDetailEndpoint():
    def test_user_signin(self,client):
        token=shop_required()
        data = {
            "address": "unittesting",
            "city": "unittesting",
            "province": "unittesting",
            "telephone": "123",
            "email": "unittesting",
            "photo": "unittesting",

        }
        res = client.patch('user/me/detail', data=json.dumps(data),content_type='application/json',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_signin_failed(self,client):
        token=shop_required()
        data = {
            "city": "unittesting",
            "province": "unittesting",
            "telephone": "123",
            "email": "unittesting",
            "photo": "unittesting",
        }
        res = client.patch('user/me/detail', data=json.dumps(data),content_type='application/json',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_user_getdetail(self,client):
        token=shop_required()
        res=client.get('user/me/detail',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_getdetail_failed(self,client):
        token=shop_required()
        res=client.get('user/me/detail',headers={'Authorization':'Bearer '+'abc'})
        res_json = json.loads(res.data)
        assert res.status_code ==500