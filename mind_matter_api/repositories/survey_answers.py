from typing import Any, Dict, List, Optional
from mind_matter_api.models.survey_answers import SurveyAnswer
from mind_matter_api.repositories.types import Repository
from mind_matter_api.models import db   

class SurveyAnswerRepository(Repository[SurveyAnswer]):
    def __init__(self):
        super().__init__(SurveyAnswer)

    def create(self, answer: SurveyAnswer) -> SurveyAnswer:
        self.session.add(answer)
        self.session.commit()
        return answer

    def get_by_id(self, resource_id: Any) -> Optional[SurveyAnswer]:
        return self.session.query(SurveyAnswer).get(resource_id)

    def get_all(self, page: int = 1, page_size: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[SurveyAnswer]:
        query = self.session.query(SurveyAnswer)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(SurveyAnswer, attr) == value)
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def update(self, resource_id: Any, data: Dict[str, Any]) -> SurveyAnswer:
        answer = self.get_by_id(resource_id)
        if not answer:
            raise ValueError("Resource not found")
        for key, value in data.items():
            setattr(answer, key, value)
        self.session.commit()
        return answer

    def delete(self, resource_id: Any) -> None:
        answer = self.get_by_id(resource_id)
        if not answer:
            raise ValueError("Resource not found")
        self.session.delete(answer)
        self.session.commit()
