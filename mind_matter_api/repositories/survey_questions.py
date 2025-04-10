from typing import Any, Dict, List, Optional
from mind_matter_api.models.surveys import SurveyQuestion
from mind_matter_api.repositories.type import Repository
from mind_matter_api.models import db   

class SurveyQuestionRepository(Repository):
    def __init__(self):
        self.session = db.session

    def create(self, question: SurveyQuestion) -> SurveyQuestion:
        self.session.add(question)
        self.session.commit()
        return question

    def get_by_id(self, resource_id: Any) -> Optional[SurveyQuestion]:
        return self.session.query(SurveyQuestion).get(resource_id)

    def get_all(self, page: int = 1, page_size: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[SurveyQuestion]:
        query = self.session.query(SurveyQuestion)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(SurveyQuestion, attr) == value)
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def update(self, resource_id: Any, data: Dict[str, Any]) -> SurveyQuestion:
        question = self.get_by_id(resource_id)
        if not question:
            raise ValueError("Resource not found")
        for key, value in data.items():
            setattr(question, key, value)
        self.session.commit()
        return question

    def delete(self, resource_id: Any) -> None:
        question = self.get_by_id(resource_id)
        if not question:
            raise ValueError("Resource not found")
        self.session.delete(question)
        self.session.commit()
