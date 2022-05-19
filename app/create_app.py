

from flask import Flask
from flask_cors import *
from .config import Config
from .models import db


app = Flask(__name__)



def register_blueprint(app):
    """ 注册蓝图 """
    from .api import api
    app.register_blueprint(api)

def create_app():
    """ 组装app """
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True)



    db.init_app(app)
    register_blueprint(app)
    return app