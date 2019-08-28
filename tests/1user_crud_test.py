import json

from . import app, client, cache, shop_required, user_required


class TestUserEndpoint():
    def test_usershop_signup(self,client):
        data = {
            "name": "unittesting",
            "username": "unittesting",
            "password": "unittesting"
        }
        res = client.post('/user/addnew', data=json.dumps(data),content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_signup(self,client):
        data = {
            "name": "unittesting2",
            "username": "unittesting2",
            "password": "unittesting2"
        }
        res = client.post('/user/addnew', data=json.dumps(data),content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_signup_failed(self,client):
        data = {
            "name": "unittesting",
            "username": "unittesting"
        }
        res = client.post('/user/addnew', data=json.dumps(data),content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_user_getme(self,client):
        token=shop_required()
        res = client.get('/user/me',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_getme_failed(self,client):
        token=shop_required()
        res = client.get('/user/me',headers={'Authorization':'Bearer '+'abc'})
        res_json = json.loads(res.data)
        assert res.status_code == 500

    def test_user_editme(self,client):
        token=shop_required()
        data = {
            "name": "unittesting",
            "username": "unittesting",
            "password": "unittesting"
        }
        res = client.put('/user/me',headers={'Authorization':'Bearer '+token}, data=json.dumps(data),content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_editme_failed(self,client):
        token=shop_required()
        data = {
            "name": "unittesting",
            "username": "unittesting",
            "password": "unittesting"
        }
        res = client.put('/user/me',headers={'Authorization':'Bearer '+'abc'}, data=json.dumps(data),content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 500