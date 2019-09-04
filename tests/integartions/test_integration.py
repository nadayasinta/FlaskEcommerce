import json
from tests import app, client, cache, shop_required, user_required, reset_database


class TestUserEndpoint():

    reset_database()

    def test_user_option1(self,client):
        res = client.options('/user/addnew')
        assert res.status_code == 200

    def test_user_option2(self,client):
        res = client.options('/user/me')
        assert res.status_code == 200

    def test_user_signup(self,client):
        data = {
            "name": "unittesting",
            "username": "unittesting",
            "password": "unittesting"
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
        assert res.status_code == 422

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
        assert res.status_code == 422





class TestUserDetailEndpoint():
    def test_user_detail_option1(self,client):
        res = client.options('/user/me/detail')
        assert res.status_code == 200

    def test_user_getdetail_failed(self,client):
        token=shop_required()
        res=client.get('user/me/detail',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

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
        assert res.status_code ==422




class TestAuthEndpoint():
    def test_auth_option1(self,client):
        res = client.options('/public/login')

        assert res.status_code == 200
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
       
    def test_user_refresh(self,client):
        token=shop_required()
        res = client.post('/public/refresh', headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200



class TestShopEndpoint():
    shopid=0

    def test_shop_option1(self,client):
        res = client.options('/shop/addnew')
        assert res.status_code == 200

    def test_shop_option2(self,client):
        res = client.options('/shop/0')
        assert res.status_code == 200

    def test_shop_option3(self,client):
        res = client.options('/shop/list')
        assert res.status_code == 200
        
    def test_shop_option4(self,client):
        res = client.options('/shop/me')
        assert res.status_code == 200

    def test_shop_option5(self,client):
        res = client.options('/shop/me/activate')
        assert res.status_code == 200

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
        res = client.post('/shop/addnew', data=json.dumps(data),content_type='application/json',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 404
  
    def test_shop_signin_failed3(self,client):
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
        assert res.status_code == 422

    def test_shop_getid(self,client):
        res = client.get('/shop/'+str(TestShopEndpoint.shopid))
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_shop_getid_failed(self,client):
        res = client.get('/shop/0')
        res_json = json.loads(res.data)
        assert res.status_code == 404


    def test_shop_getlist(self,client):
        res = client.get('/shop/list')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_shop_getme(self,client):
        token=shop_required()
        res = client.get('/shop/me',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_shop_getme_failed(self,client):
        token=user_required()
        res = client.get('/shop/me',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)

        assert res.status_code == 403
    def test_shop_getme_edit(self,client):
        token=shop_required()
        data = {
            "name": "unittesting",
            "address": "unittesting",
            "city": "unittesting",
            "province": "unittesting",
            "telephone": "unittesting",
            "photo": "unittesting",
        }
        res = client.put('/shop/me', data=json.dumps(data),content_type='application/json',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_shop_activate(self,client):
        token=shop_required()
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

    def test_shop_activate_failed(self,client):
        token=user_required()
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
        assert res.status_code == 403


    def test_shop_deactivate(self,client):
        token=shop_required() 
        res = client.delete('shop/me/activate',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_item_list_shop_deactivate(self,client):
        token=shop_required()
        res = client.get('item/listall', headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_item_add_shop_deactivate(self,client):
        token=shop_required()
        data = {
            "name": "unittesting",
            "qty": "1",
            "price": "1",
            "category": "unittesting",
            "description": "unittesting",
            "detail": "unittestingnew",
        }
        res = client.post('/item/me', data=json.dumps(data),content_type='application/json',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_item_edit_shop_deactivate (self,client):
        token=shop_required()
        data = {
            "name": "unittesting",
            "qty": "1",
            "price": "1",
            "category": "unittesting",
            "description": "unittesting",
            "detail": "unittestingnew",
        }
        res = client.put('/item/me/'+str(TestItemEndpoint.itemid), data=json.dumps(data),content_type='application/json',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_item_deactivate_shop_deactivate(self,client):
        token=shop_required()
        res = client.delete('/item/me/activate/'+str(TestItemEndpoint.itemid), headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_item_activate_shop_deactivate(self,client):
        token=shop_required()
        res = client.put('/item/me/activate/'+str(TestItemEndpoint.itemid), headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_shop_deactivate_failed(self,client):
        token=user_required() 
        res = client.delete('shop/me/activate',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 403

    def test_shop_activate(self,client):
        token=shop_required()
        res = client.put('shop/me/activate',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_shop_activate_failed(self,client):
        token=user_required()
        res = client.put('shop/me/activate',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 403



class TestItemEndpoint():
    itemid=0
    cartid=0

    def test_item_option1(self,client):
        res = client.options('/item/0')
        assert res.status_code == 200

    def test_item_option2(self,client):
        res = client.options('/item/list')
        assert res.status_code == 200

    def test_item_option3(self,client):
        res = client.options('/item/listall')
        assert res.status_code == 200

    def test_item_option4(self,client):
        res = client.options('/item/me')
        assert res.status_code == 200

    def test_item_option5(self,client):
        res = client.options('/item/me/activate/0')
        assert res.status_code == 200

    def test_item_option6(self,client):
        res = client.options('/item/rent/0')
        assert res.status_code == 200

    def test_item_detail_notfound(self,client):
        res = client.get('item/'+str(TestItemEndpoint.itemid))
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_item_add(self,client):
        token=shop_required()
        data = {
            "name": "unittesting",
            "qty": "20",
            "price": "1",
            "category": "unittesting",
            "description": "unittesting",
            "detail": "unittestingnew",
        }
        res = client.post('/item/me', data=json.dumps(data),content_type='application/json',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        TestItemEndpoint.itemid=res_json["id"]
        assert res.status_code == 200

    def test_item_add_qty0(self,client):
        token=shop_required()
        data = {
            "name": "unittesting",
            "qty": "0",
            "price": "1",
            "category": "unittesting",
            "description": "unittesting",
            "detail": "unittestingnew",
        }
        res = client.post('/item/me', data=json.dumps(data),content_type='application/json',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_item_edit(self,client):
        token=shop_required()
        data = {
            "name": "unittesting",
            "qty": "1",
            "price": "1",
            "category": "unittesting",
            "description": "unittesting",
            "detail": "unittestingnew",
        }
        res = client.put('/item/me/'+str(TestItemEndpoint.itemid), data=json.dumps(data),content_type='application/json',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_item_list(self,client):
        res = client.get('item/list')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_item_detail(self,client):
        res = client.get('item/'+str(TestItemEndpoint.itemid))
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_item_list_shop(self,client):
        token=shop_required()
        res = client.get('item/listall', headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_item_activate_failed(self,client):
        token=shop_required()
        res = client.put('/item/me/activate/'+str(TestItemEndpoint.itemid), headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_item_deactivate(self,client):
        token=shop_required()
        res = client.delete('/item/me/activate/'+str(TestItemEndpoint.itemid), headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_item_deactivate_failed(self,client):
        token=shop_required()
        res = client.delete('/item/me/activate/'+str(TestItemEndpoint.itemid), headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_item_activate(self,client):
        token=shop_required()
        res = client.put('/item/me/activate/'+str(TestItemEndpoint.itemid), headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_item_cart_qty0(self,client):
        token=shop_required()
        data = {
            "date": "2019-08-02",
            "duration": "1",
            "qty": "0",
        }
        res = client.patch('/item/rent/'+str(TestItemEndpoint.itemid), data=json.dumps(data),content_type='application/json', headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_item_cart_qtymin(self,client):
        token=shop_required()
        data = {
            "date": "2019-08-02",
            "duration": "1",
            "qty": "1110",
        }
        res = client.patch('/item/rent/1110', data=json.dumps(data),content_type='application/json', headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 404


    def test_item_cart(self,client):
        token=shop_required()
        data = {
            "date": "2019-08-02",
            "duration": "1",
            "qty": "1",
        }
        res = client.patch('/item/rent/'+str(TestItemEndpoint.itemid), data=json.dumps(data),content_type='application/json', headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        TestItemEndpoint.cartid=res_json["id"]
        assert res.status_code == 200



class TestCartEndpoint():
    cartid2=0
    transactionid=0

    def test_cart_option1(self,client):
        res = client.options('/cart/0')
        assert res.status_code == 200

    def test_cart_option2(self,client):
        res = client.options('/cart/list')
        assert res.status_code == 200

    def test_cart_option3(self,client):
        res = client.options('/cart/checkout')
        assert res.status_code == 200

    def test_cart_delete1(self,client):
        token=shop_required()
        res = client.delete('/cart/'+str(TestItemEndpoint.cartid),headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_cart_create(self,client):
        token=shop_required()
        data = {
            "date": "2019-08-02",
            "duration": "1",
            "qty": "1",
        }
        res = client.patch('/item/rent/'+str(TestItemEndpoint.itemid), data=json.dumps(data),content_type='application/json', headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        TestCartEndpoint.cartid2=res_json["id"]
        assert res.status_code == 200

    def test_cart_detail(self,client):
        token=shop_required()
        res = client.get('/cart/'+str(TestCartEndpoint.cartid2), headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_cart_edit(self,client):
        token=shop_required()
        data = {
            "date": "2019-08-02",
            "duration": "1",
            "qty": "1",
        }
        res = client.put('/cart/'+str(TestCartEndpoint.cartid2), data=json.dumps(data),content_type='application/json',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200


    def test_cart_list(self,client):
        token=shop_required()
        res = client.get('/cart/list',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_cart_checkout(self,client):
        token=shop_required()
        res = client.post('/cart/checkout',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        print(res_json)
        TestCartEndpoint.transactionid=res_json[0]["id"]
        assert res.status_code == 200



class TestTransactionEndpoint():
    def test_transaction_option1(self,client):
        res = client.options('/transaction/me/0')
        assert res.status_code == 200

    def test_transaction_option2(self,client):
        res = client.options('/transaction/me/list')
        assert res.status_code == 200

    def test_transaction_option3(self,client):
        res = client.options('/transaction/shop/0')
        assert res.status_code == 200

    def test_transaction_option4(self,client):
        res = client.options('/transaction/shop/list')
        assert res.status_code == 200

    def test_transaction_option5(self,client):
        res = client.options('/transaction/shop/done/0')
        assert res.status_code == 200

    def test_transaction_me_detail(self,client):
        token=shop_required()
        res = client.get('/transaction/me/'+str(TestCartEndpoint.transactionid),headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_transaction_me_detail_failed(self,client):
        token=shop_required()
        res = client.get('/transaction/me/0',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_transaction_me_list(self,client):
        token=shop_required()
        res = client.get('/transaction/me/list',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_transaction_shop_detail(self,client):
        token=shop_required()
        res = client.get('/transaction/shop/'+str(TestCartEndpoint.transactionid),headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_transaction_shop_list(self,client):
        token=shop_required()
        res = client.get('/transaction/shop/list',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_transaction_shop_donepay(self,client):
        token=shop_required()
        res = client.put('/transaction/shop/'+str(TestCartEndpoint.transactionid),headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_transaction_shop_donerent(self,client):
        token=shop_required()
        res = client.put('/transaction/shop/done/'+str(TestCartEndpoint.transactionid),headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_transaction_shop_delete(self,client):
        token=shop_required()
        res = client.delete('/transaction/shop/'+str(TestCartEndpoint.transactionid),headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200





class TestUserDeleteEndpoint():
    def test_user_deletme_failed(self,client):
        token=shop_required()
        res = client.delete('/user/me',headers={'Authorization':'Bearer '+'abc'})
        res_json = json.loads(res.data)
        assert res.status_code == 422

    def test_user_deleteme(self,client):
        token=shop_required()
        res = client.delete('/user/me',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_deleteme2(self,client):
        token=user_required()
        res = client.delete('/user/me',headers={'Authorization':'Bearer '+token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
