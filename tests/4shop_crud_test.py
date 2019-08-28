import json

from . import app, client, cache, shop_required,  user_required


class TestShopEndpoint():
    shopid=0
    def test_shop_signin(self,client):
        token=shop_required()
        data = {
            "name": "unittesting",
            "address": "unittesting",
            "city": "unittesting",
            "province": "unittesting",
            "telephone": "unittesting",
            "photo": "unittesting",
        }
        res = client.post('/shop/addnew', data=json.dumps(data),content_type='application/json',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        TestShopEndpoint.shopid=res_json["id"]
        assert res.status_code == 200

    def test_shop_signin_failed(self,client):
        token=shop_required()
        data = {
            "address": "unittesting",
            "city": "unittesting",
            "province": "unittesting",
            "telephone": "unittesting",
            "photo": "unittesting",
        }
        res = client.post('/shop/addnew', data=json.dumps(data),content_type='application/json',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 400
  
    def test_shop_signin_failed2(self,client):
        token=shop_required()
        data = {
            "name": "unittesting",
            "address": "unittesting",
            "city": "unittesting",
            "province": "unittesting",
            "telephone": "unittesting",
            "photo": "unittesting",
        }
        res = client.post('/shop/addnew', data=json.dumps(data),content_type='application/json',headers={'Authorization':'Bearer '+'abc'})
        res_json = json.loads(res.data)
        assert res.status_code == 500

    def test_shop_getid(self,client):
        res = client.get('/shop'+str(TestShopEndpoint.shopid))
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_shop_getlist(self,client):
        res = client.get('/shop/list')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_shop_getme(self,client):
        token=shop_required()
        res = client.get('/shop/me',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_shop_activate(self,client):
        token=shop_required()
        # res = client.post('public/refresh',headers={'Authorization':'Bearer '+token})
        # newtoken = json.loads(res.data)["token"]       
        data = {
            "name": "unittesting",
            "address": "unittesting",
            "city": "unittesting",
            "province": "unittesting",
            "telephone": "unittesting",
            "photo": "unittestingnew",
        }
        res = client.put('/shop/me', data=json.dumps(data),content_type='application/json',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_shop_deactivate(self,client):
        token=shop_required()
        # res = client.post('public/refresh',headers={'Authorization':'Bearer '+token})
        # newtoken = json.loads(res.data)["token"]   
        res = client.delete('shop/me/activate',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_shop_activate(self,client):
        token=shop_required()
        # res = client.post('public/refresh',headers={'Authorization':'Bearer '+token})
        # newtoken = json.loads(res.data)["token"]   
        res = client.put('shop/me/activate',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # def test_shop_deactivate2(self,client):
    #     token=shop_required()
    #     res = client.delete('shop/me/activate',headers={'Authorization':'Bearer '+token})
    #     res_json = json.loads(res.data)
    #     assert res.status_code == 200