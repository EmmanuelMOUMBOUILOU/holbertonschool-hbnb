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
        if not current_user or not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.get_json()
        if not data or not data.get('name'):
            return {'error': 'Amenity name required'}, 400

        try:
            new_amenity = create_amenity(data)
        except Exception as e:
            return {'error': str(e)}, 400

        return {
            'message': 'Amenity created',
            'amenity': new_amenity.to_dict()
        }, 201

@api.route('/<string:amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user or not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.get_json()
        amenity = get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        try:
            updated_amenity = update_amenity(amenity_id, data)
        except Exception as e:
            return {'error': str(e)}, 400

        return {
            'message': 'Amenity updated',
            'amenity': updated_amenity.to_dict()
        }, 200

