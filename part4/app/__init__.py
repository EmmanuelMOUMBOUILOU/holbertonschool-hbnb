from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api
from app.api.v1.auth import api as auth_ns
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as place_ns
from app.api.v1.amenities import api as amenity_ns
from app.api.v1.reviews import api as review_ns
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from app.extensions.db import db
import config
from app.services.admin_user import api as admin_user_api
from app.services.admin_amenity import api as admin_amenity_api
from app.services.admin_place import api as admin_place_api

jwt = JWTManager()
bcrypt = Bcrypt()
db = SQLAlchemy()
db.init_app(app)

api.init_app(app)
app.register_blueprint(admin_user_api.blueprint)
app.register_blueprint(admin_amenity_api.blueprint)
app.register_blueprint(admin_place_api.blueprint)


def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')
    app.config.from_object(config_class)
    jwt.init_app(app)

    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(place_ns, path='/api/v1/places')
    api.add_namespace(amenity_ns, path='/api/v1/amenities')
    api.add_namespace(review_ns, path='/api/v1/reviews')
    bcrypt.init_app(app)
    db.init_app(app)
    return app
