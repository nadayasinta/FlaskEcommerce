from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from flask_cors import CORS
from datetime import timedelta
from functools import wraps

import json

app = Flask(__name__)
CORS(app)

app.config['APP_DEBUG'] = True

############################
# JWT 
############################
app.config['JWT_SECRET_KEY'] = 'thisissecret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

def shop_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status'] != True:
            return {'status': 'FORBIDDEN', 'message': 'Buat toko dulu'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper



##########################
# DATABASE
##########################
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:alta321@localhost:3306/ecommerce_project'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)



###################
# LOGGING
###################
@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except:
        requestData = request.args.to_dict()

    if response.status_code == 200:
        app.logger.warning('REQUEST_LOG\t%s', 
            json.dumps({
                'method': request.method,
                'code': response.status,
                'uri': request.full_path,
                'request': requestData,
                'response': json.loads(response.data.decode('utf-8'))
            })
        )

    return response



###############
# RESOURCES
###############
from blueprint.auth import bp_auth
from blueprint.user.resource import bp_user
from blueprint.user_detail.resource import bp_user_detail
from blueprint.shop.resource import bp_shop
from blueprint.item.resource import bp_item
from blueprint.cart.resource import bp_cart
from blueprint.transaction.resource import bp_transaction

app.register_blueprint(bp_auth, url_prefix='/public')
app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_user_detail, url_prefix='/user')
app.register_blueprint(bp_shop, url_prefix='/shop')
app.register_blueprint(bp_item, url_prefix='/item')
app.register_blueprint(bp_cart, url_prefix='/cart')
app.register_blueprint(bp_transaction, url_prefix='/transaction')

db.create_all()