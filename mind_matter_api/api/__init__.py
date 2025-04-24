# mind_matter_api/api/__init__.py
# users
from mind_matter_api.api.users import init_user_routes
from mind_matter_api.repositories.users import UserRepository
from mind_matter_api.services.users import UserService

# surveys
from mind_matter_api.api.surveys import init_survey_routes
from mind_matter_api.repositories.surveys import SurveyRepository
from mind_matter_api.services.surveys import SurveyService

def register_routes(app):
    # --- wire up your services ---
    app.user_service = UserService(UserRepository())

    # --- mount your route init functions ---
    init_user_routes(app)


    app.survey_service = SurveyService(SurveyRepository())
    init_survey_routes(app)
