from flask import jsonify, request, current_app
from marshmallow import ValidationError

from mind_matter_api.services.campaigns import CampaignsService
from mind_matter_api.utils.decorators import require_auth, require_owner
from mind_matter_api.utils.auth import is_user_owner, is_user_admin
import logging

logging.basicConfig(level=logging.DEBUG)

def init_campaigns_routes(app):
    campaign_service: CampaignsService = app.campaigns_service

    @app.route('/campaigns', methods=['GET'])
    @require_auth
    def get_campaigns(user_id):
        return campaign_service.get_campaigns(user_id)   
    
    @app.route('/campaigns/<int:campaign_id>/survey-responses-count', methods=['GET'])
    @require_auth
    def get_survey_responses_count(campaign_id):
        return campaign_service.get_survey_responses_count(campaign_id)
    
    @app.route('/campaigns/<int:campaign_id>/participation', methods=['GET'])
    @require_auth
    def get_campaign_participation(campaign_id):
        return campaign_service.get_campaign_participation(campaign_id)
    