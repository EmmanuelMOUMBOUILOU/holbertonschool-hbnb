from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.services.facade import create_amenity, get_amenity, update_amenity

api = Namespace('admin_amenities', path='/api/v1/amenities')

@api.route('/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        if not data or not data.get('name'):
            return {'error': 'Amenity name required'}, 400

        new_amenity = create_amenity(data)
        return {
            'message': 'Amenity created',
            'amenity': new_amenity.to_dict()
        }, 201

@api.route('/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        amenity = get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        updated_amenity = update_amenity(amenity_id, data)
        return {
            'message': 'Amenity updated',
            'amenity': updated_amenity.to_dict()
        }, 200
