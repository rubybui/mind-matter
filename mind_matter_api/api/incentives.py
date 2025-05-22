from flask import jsonify, request
from marshmallow import ValidationError

from mind_matter_api.services.incentives import IncentiveService
from mind_matter_api.utils.decorators import require_auth, require_owner
from mind_matter_api.utils.auth import is_user_owner, is_user_admin
import logging

logging.basicConfig(level=logging.DEBUG)

def init_incentives_routes(app):
    incentive_service: IncentiveService = app.incentive_service

    @app.route('/campaigns/<int:campaign_id>/incentives', methods=['GET'])
    @require_auth
    def get_campaign_incentives(campaign_id):
        """Get all incentives for a specific campaign"""
        incentives = incentive_service.get_campaign_incentives(campaign_id)
        return jsonify(incentives)

    @app.route('/campaigns/<int:campaign_id>/incentives', methods=['POST'])
    @require_auth
    def create_campaign_incentive(campaign_id):
        """Create a new incentive for a campaign"""
        try:
            data = request.get_json()
            data['campaign_id'] = campaign_id
            incentive = incentive_service.create_incentive(data)
            return jsonify(incentive), 201
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/campaigns/<int:campaign_id>/incentives/<int:incentive_id>', methods=['PUT'])
    @require_auth
    def update_campaign_incentive(campaign_id, incentive_id):
        """Update an existing incentive"""
        try:
            data = request.get_json()
            incentive = incentive_service.update_incentive(incentive_id, data)
            return jsonify(incentive)
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/campaigns/<int:campaign_id>/incentives/<int:incentive_id>', methods=['DELETE'])
    @require_auth
    def delete_campaign_incentive(campaign_id, incentive_id):
        """Delete an incentive"""
        incentive_service.delete_incentive(incentive_id)
        return '', 204
