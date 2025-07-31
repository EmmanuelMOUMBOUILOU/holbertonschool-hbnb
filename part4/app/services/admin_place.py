from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.services.facade import get_place, update_place, delete_place

api = Namespace('admin_places', path='/api/v1/places')

@api.route('/<string:place_id>')
class AdminPlaceResource(Resource):
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Unauthorized'}, 401

        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        data = request.get_json()
        if not data:
            return {'error': 'No input data provided'}, 400

        try:
            updated_place = update_place(place_id, data)
        except Exception as e:
            return {'error': str(e)}, 400

        return {
            'message': 'Place updated',
            'place': updated_place.to_dict()
        }, 200

    @jwt_required()
    def delete(self, place_id):
        current_user = get_jwt_identity()
        if not current_user:
            return {'error': 'Unauthorized'}, 401

        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            delete_place(place_id)
        except Exception as e:
            return {'error': str(e)}, 400

        return {'message': 'Place deleted'}, 200

