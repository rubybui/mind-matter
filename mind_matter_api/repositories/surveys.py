from typing import Any, Dict, List, Optional
from mind_matter_api.models.surveys import Survey
from mind_matter_api.repositories.type import Repository
from mind_matter_api.models import db   

class SurveyRepository(Repository):
    def __init__(self):
        self.session = db.session

    def create(self, survey: Survey) -> Survey:
        self.session.add(survey)
        self.session.commit()
        return survey

    def get_by_id(self, resource_id: Any) -> Optional[Survey]:
        return self.session.query(Survey).get(resource_id)

    def get_all(self, page: int = 1, page_size: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Survey]:
        query = self.session.query(Survey)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(Survey, attr) == value)
        return query.offset((page - 1) * page_size).limit(page_size).all()

    def update(self, resource_id: Any, data: Dict[str, Any]) -> Survey:
        survey = self.get_by_id(resource_id)
        if not survey:
            raise ValueError("Resource not found")
        for key, value in data.items():
            setattr(survey, key, value)
        self.session.commit()
        return survey

    def delete(self, resource_id: Any) -> None:
        survey = self.get_by_id(resource_id)
        if not survey:
            raise ValueError("Resource not found")
        self.session.delete(survey)
        self.session.commit()

    def get_by_user_id(self, user_id: str) -> Optional[Survey]:
        return self.session.query(Survey).filter(Survey.user_id == user_id).first()
    def get_by_survey_id(self, survey_id: str) -> Optional[Survey]:
        return self.session.query(Survey).filter(Survey.survey_id == survey_id).first()      
    def get_by_survey_name(self, survey_name: str) -> Optional[Survey]:
        return self.session.query(Survey).filter(Survey.survey_name == survey_name).first()
    def get_by_survey_type(self, survey_type: str) -> Optional[Survey]:
        return self.session.query(Survey).filter(Survey.survey_type == survey_type).first() 
        