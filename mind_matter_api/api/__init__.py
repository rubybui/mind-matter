# mind_matter_api/api/__init__.py
# users
from mind_matter_api.api.users import init_user_routes
from mind_matter_api.repositories.users import UserRepository
from mind_matter_api.services.users import UserService

# surveys
from mind_matter_api.api.surveys import init_survey_routes
from mind_matter_api.repositories.surveys import SurveyRepository
from mind_matter_api.repositories.survey_answers import SurveyAnswerRepository
from mind_matter_api.repositories.survey_questions import SurveyQuestionRepository
from mind_matter_api.repositories.survey_responses import SurveyResponseRepository
from mind_matter_api.services.surveys import SurveyService

# campaigns
from mind_matter_api.api.campaigns import init_campaigns_routes
from mind_matter_api.repositories.campaigns import CampaignRepository
from mind_matter_api.services.campaigns import CampaignsService

# email
from mind_matter_api.api.email import init_email_routes

# emergency contacts
from mind_matter_api.api.emergency_contacts import init_emergency_contacts_routes
from mind_matter_api.repositories.emergency_contacts import EmergencyContactRepository
from mind_matter_api.services.emergency_contacts import EmergencyContactsService

def register_routes(app):
    # --- wire up your services ---
    app.user_service = UserService(UserRepository())

    # --- mount your route init functions ---
    init_user_routes(app)
    init_email_routes(app)

    app.survey_service = SurveyService(SurveyRepository(), 
                                      SurveyQuestionRepository(), 
                                      SurveyResponseRepository(), 
                                      SurveyAnswerRepository())
    init_survey_routes(app)

    # Initialize emergency contacts service and routes
    app.emergency_contacts_service = EmergencyContactsService(EmergencyContactRepository())
    init_emergency_contacts_routes(app)

    # Initialize campaigns service and routes
    app.campaign_service = CampaignsService(CampaignRepository())
    init_campaigns_routes(app)
