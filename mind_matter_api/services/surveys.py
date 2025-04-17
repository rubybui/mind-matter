
from mind_matter_api.repositories.survey import SurveyRepository
from mind_matter_api.models.surveys import Survey, SurveyQuestion, SurveyResponse
from mind_matter_api.schemas.surveys import SurveySchema


class SurveyService(BaseService):
    def __init__(self, survey_repository: SurveyRepository):
        self.survey_repository = survey_repository

    def get_survey(self, survey_id: str) -> Survey:
        survey = self.survey_repository.get(survey_id)
        return survey
    def create_survey(self, survey_data: SurveySchema) -> Survey:
        new_survey = Survey(**survey_data)
        created_survey = self.survey_repository.create(new_survey)
        return created_survey
    def get_surveys(self) -> list[Survey]:
        surveys = self.survey_repository.get_all()
        return surveys
    def get_survey_questions(self, survey_id: str) -> list[SurveyQuestion]:
        survey = self.survey_repository.get(survey_id)
        return survey.questions
    def get_survey_responses(self, survey_id: str) -> list[SurveyResponse]:
        survey = self.survey_repository.get(survey_id)
        return survey.responses
    def submit_survey_response(self, survey_id: str, response_data: dict) -> SurveyResponse:
        survey = self.survey_repository.get(survey_id)
        new_response = SurveyResponse(**response_data)
        survey.responses.append(new_response)
        self.survey_repository.update(survey)
        return new_response
    def update_survey(self, survey_id: str, survey_data: SurveySchema) -> Survey:
        survey = self.survey_repository.get(survey_id)
        survey.update(**survey_data)
        self.survey_repository.update(survey)
        return survey

    def get_survey_by_user_id(self, user_id: str) -> Survey:
        survey = self.survey_repository.get_by_user_id(user_id)
        return survey