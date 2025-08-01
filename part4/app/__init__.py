from flask import Flask, request, jsonify
from flask_restx import Api
from flask_cors import CORS
import config
from app.extensions import db, bcrypt, jwt


def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['DEBUG'] = True

    # Désactive redirections automatiques slash
    app.url_map.strict_slashes = False

    # CORS global via flask-cors
    CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:5500"]}}, supports_credentials=True)

    # JWT config
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    app.config['JWT_SECRET_KEY'] = config_class.JWT_SECRET_KEY

    # Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # API & namespaces
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')

    from app.api.v1.auth import api as auth_ns
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as place_ns
    from app.api.v1.amenities import api as amenity_ns
    from app.api.v1.reviews import api as review_ns

    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(place_ns, path='/api/v1/places')
    api.add_namespace(amenity_ns, path='/api/v1/amenities')
    api.add_namespace(review_ns, path='/api/v1/reviews')

    from app.services.admin_user import api as admin_user_api
    from app.services.admin_amenity import api as admin_amenity_api
    from app.services.admin_place import api as admin_place_api

    api.add_namespace(admin_user_api, path='/api/v1/admin/users')
    api.add_namespace(admin_amenity_api, path='/api/v1/admin/amenities')
    api.add_namespace(admin_place_api, path='/api/v1/admin/places')

    # Réponse aux requêtes OPTIONS (préflight CORS) — fix pour frontend
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5500')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        return response

    return app
