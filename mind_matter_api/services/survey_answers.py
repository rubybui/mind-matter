
from mind_matter_api.repositories.survey_answers import SurveyAnswerRepository

from mind_matter_api.models.survey_answers import SurveyAnswer
from mind_matter_api.schemas.survey_answers import  SurveyAnswerBodySchema

from mind_matter_api.services.types import BaseService
from mind_matter_api.models.surveys import Survey
from mind_matter_api.models.users import User
from mind_matter_api.models.surveys import SurveyQuestion, SurveyResponse, SurveyResponseAnswer, SurveyResponseAnswerOption

class SurveyAnswerService(BaseService):
    def __init__(self, survey_answer_repository: SurveyAnswerRepository):
        self.survey_answer_repository = survey_answer_repository

    def get_survey_answer(self, survey_answer_id: str) -> SurveyAnswer:
        survey_answer = self.survey_answer_repository.get(survey_answer_id)
        return survey_answer

    def create_survey_answer(self, survey_answer_data: SurveyAnswerBodySchema) -> SurveyAnswer:
        new_survey_answer = SurveyAnswer(**survey_answer_data)
        created_survey_answer = self.survey_answer_repository.create(new_survey_answer)
        return created_survey_answer
    def get_survey_answers(self) -> list[SurveyAnswer]:
        survey_answers = self.survey_answer_repository.get_all()
        return survey_answers
    def get_survey_answer_by_user_id(self, user_id: str) -> SurveyAnswer:     
        survey_answer = self.survey_answer_repository.get_by_user_id(user_id)
        return survey_answer
    def get_survey_answer_by_survey_id(self, survey_id: str) -> SurveyAnswer:
        survey_answer = self.survey_answer_repository.get_by_survey_id(survey_id)
        return survey_answer
    def create_survey_answer(self, survey_answer_data: SurveyAnswerBodySchema) -> SurveyAnswer:
        new_survey_answer = SurveyAnswer(**survey_answer_data)
        created_survey_answer = self.survey_answer_repository.create(new_survey_answer)
        return created_survey_answer
    def update_survey_answer(self, survey_answer_id: str, survey_answer_data: SurveyAnswerBodySchema) -> SurveyAnswer:  
        survey_answer = self.survey_answer_repository.get(survey_answer_id)
        survey_answer.update(**survey_answer_data)
        self.survey_answer_repository.update(survey_answer)
        return survey_answer
    def delete_survey_answer(self, survey_answer_id: str) -> None:
        survey_answer = self.survey_answer_repository.get(survey_answer_id)
        self.survey_answer_repository.delete(survey_answer)