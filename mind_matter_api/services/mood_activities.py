from mind_matter_api.services.types import BaseService
from mind_matter_api.models.mood_activities import MoodActivities
from mind_matter_api.repositories.mood_activities import MoodActivitiesRepository

class MoodActivitiesService(BaseService):
    def __init__(self, mood_activities_repository: MoodActivitiesRepository):
        self.mood_activities_repository = mood_activities_repository

    def get_mood_activities(self, user_id: str) -> MoodActivities:
        mood_activities = self.mood_activities_repository.get(user_id)
        return mood_activities

    def create_mood_activities(self, user_data: MoodActivities) -> MoodActivities:
        new_mood_activities = MoodActivities(**user_data)
        created_mood_activities = self.mood_activities_repository.create(new_mood_activities)
        return created_mood_activities
    def update_mood_activities(self, user_id: str, mood_activities_data: MoodActivities) -> MoodActivities:
        mood_activities = self.mood_activities_repository.get(user_id)
        mood_activities.update(**mood_activities_data)
        self.mood_activities_repository.update(mood_activities)
        return mood_activities
    def delete_mood_activities(self, user_id: str) -> None: 
        mood_activities = self.mood_activities_repository.get(user_id)
        self.mood_activities_repository.delete(mood_activities)