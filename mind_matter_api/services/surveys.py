from typing import Any, Dict, List, Optional
from mind_matter_api.repositories.surveys import SurveyRepository
from mind_matter_api.repositories.survey_questions import SurveyQuestionRepository
from mind_matter_api.repositories.survey_responses import SurveyResponseRepository
from mind_matter_api.repositories.survey_answers import SurveyAnswerRepository
from mind_matter_api.models.surveys import Survey
from mind_matter_api.models.surveys import SurveyQuestion, SurveyResponse
from mind_matter_api.models.survey_answers import SurveyAnswer

class SurveyService:
    """
    Service layer for Survey operations, including surveys, questions, responses, and answers.
    """
    def __init__(
        self,
        survey_repo: SurveyRepository,
        question_repo: SurveyQuestionRepository,
        response_repo: SurveyResponseRepository,
        answer_repo: SurveyAnswerRepository
    ):
        self.survey_repo = survey_repo
        self.question_repo = question_repo
        self.response_repo = response_repo
        self.answer_repo = answer_repo

    # --- Survey CRUD ---
    def get_all(self,
                page: int = 1,
                page_size: int = 10,
                filters: Optional[Dict[str, Any]] = None
               ) -> List[Survey]:
        """
        Retrieve a paginated list of surveys, optionally filtered.
        """
        return self.survey_repo.get_all(page, page_size, filters)

    def get_by_id(self, survey_id: Any) -> Optional[Survey]:
        """Retrieve a single survey by its ID."""
        return self.survey_repo.get_by_id(survey_id)

    def create(self, data: Dict[str, Any]) -> Survey:
        """Create a new survey with the given data."""
        survey = Survey(**data)
        return self.survey_repo.create(survey)

    def update(self, survey_id: Any, data: Dict[str, Any]) -> Survey:
        """Update an existing survey with new data."""
        return self.survey_repo.update(survey_id, data)

    def delete(self, survey_id: Any) -> None:
        """Delete a survey by its ID."""
        self.survey_repo.delete(survey_id)

    # --- Question CRUD ---
    def get_questions(self, survey_id: Any, page: int = 1, page_size: int = 10) -> List[SurveyQuestion]:
        """Retrieve paginated questions for a given survey."""
        return self.question_repo.get_all(page=page, page_size=page_size, filters={'survey_id': survey_id})

    def get_questions_count(self, survey_id: Any) -> int:
        """Get total count of questions for a survey."""
        return self.question_repo.get_count(filters={'survey_id': survey_id})

    def get_question_by_id(self, question_id: Any) -> Optional[SurveyQuestion]:
        """Retrieve a question by its ID."""
        return self.question_repo.get_by_id(question_id)

    def create_question(self, data: Dict[str, Any]) -> SurveyQuestion:
        """Create a new survey question."""
        question = SurveyQuestion(**data)
        return self.question_repo.create(question)

    def update_question(self, question_id: Any, data: Dict[str, Any]) -> SurveyQuestion:
        """Update an existing question."""
        return self.question_repo.update(question_id, data)

    def delete_question(self, question_id: Any) -> None:
        """Delete a question by ID."""
        self.question_repo.delete(question_id)

    # --- Response CRUD ---
    def get_responses(self, survey_id: Any) -> List[SurveyResponse]:
        """Retrieve all responses for a given survey."""
        return self.response_repo.get_all(filters={'survey_id': survey_id})

    def get_response_by_id(self, response_id: Any) -> Optional[SurveyResponse]:
        """Retrieve a single response by ID."""
        return self.response_repo.get_by_id(response_id)

    def create_response(self, data: Dict[str, Any]) -> SurveyResponse:
        """Create a new survey response."""
        response = SurveyResponse(**data)
        return self.response_repo.create(response)

    def update_response(self, response_id: Any, data: Dict[str, Any]) -> SurveyResponse:
        """Update an existing response."""
        return self.response_repo.update(response_id, data)

    def delete_response(self, response_id: Any) -> None:
        """Delete a response by ID."""
        self.response_repo.delete(response_id)

    # --- Answer CRUD ---
    def get_answers(self, response_id: Any) -> List[SurveyAnswer]:
        """Retrieve all answers for a given response."""
        return self.answer_repo.get_all(filters={'response_id': response_id})

    def get_answer_by_id(self, answer_id: Any) -> Optional[SurveyAnswer]:
        """Retrieve a single answer by ID."""
        return self.answer_repo.get_by_id(answer_id)

    def create_answer(self, data: Dict[str, Any]) -> SurveyAnswer:
        """Create a new survey answer."""
        answer = SurveyAnswer(**data)
        return self.answer_repo.create(answer)

    def update_answer(self, answer_id: Any, data: Dict[str, Any]) -> SurveyAnswer:
        """Update an existing answer."""
        return self.answer_repo.update(answer_id, data)

    def delete_answer(self, answer_id: Any) -> None:
        """Delete an answer by ID."""
        self.answer_repo.delete(answer_id)
