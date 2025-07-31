from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'place_id': fields.String(required=True)
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = dict(api.payload)
        data["user_id"] = current_user
        place = facade.get_place(data["place_id"])
        review = facade.get_review_by_user_and_place(current_user, data["place_id"])
        try:
            if current_user == place.owner_id:
                return {'error': "you cannot review your own place."}, 400
            if review:
                return {'error': "You have already reviewed this place."}, 400
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        reviews = [r.to_dict() for r in facade.get_all_reviews()]
        return reviews, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @jwt_required()
    def put(self, review_id):
        current_user = get_jwt_identity()
        data = dict(api.payload)
        data["user_id"] = current_user
        if not review:
            return {'error': 'Review not found'}, 404
        if current_user != review.user_id:
                return {'error': "Unauthorized action."}, 403
        try:
            updated_review = facade.update_review(review_id, data)
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    def delete(self, review_id):
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if current_user != review.user_id:
            return {'error': "Unauthorized action."}, 403
        deleted = facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    def get(self, place_id):
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [r.to_dict() for r in reviews], 200
        except ValueError as e:
            return {'error': str(e)}, 404
