from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
api = Api()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    try:
        app.config.from_pyfile('config.py')
    except:
        pass

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)


    import apirest.models
    with app.app_context():
        db.create_all()

    import apirest.views
    import apirest.routes
    api.init_app(app)

    return app