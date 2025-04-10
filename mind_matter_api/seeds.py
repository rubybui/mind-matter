from flask import current_app
from mind_matter_api.extensions import db
from tests.factories import UserFactory

def seed_database(users=10, recipes=3):
    """Seed the database with mock data."""

    with current_app.app_context():
        try:
            db.drop_all()  # Reset the database
            db.create_all()

            for _ in range(users):
                user = UserFactory()
                db.session.add(user)  # Explicitly add user to the session

            db.session.commit()
            print("Database seeded successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error during seeding: {e}")
