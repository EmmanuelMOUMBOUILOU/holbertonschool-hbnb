from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.v1.views import api
from models import facade
from models.amenity import Amenity

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        if not get_jwt_identity().get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.get_json()
        name = data.get('name')
        if not name:
            return {'error': 'Amenity name is required'}, 400

        amenity = Amenity(name=name)
        facade.save_amenity(amenity)
        return {'message': 'Amenity created', 'id': amenity.id}, 201


@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        if not get_jwt_identity().get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        data = request.get_json()
        if 'name' in data:
            amenity.name = data['name']
        facade.save_amenity(amenity)
        return {'message': 'Amenity updated'}, 200
