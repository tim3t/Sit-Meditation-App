import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Sit

os.environ['DATABASE_URL'] = "postgresql:///sit_db_test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.uid = 12345
        u = User.signup("Tester123", "password", "Chester", "Tester", "chester@email.com")
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_sit_model(self):
        s = Sit(user_id=self.uid, duration=30, sit_title="Test Sit 1", sit_body="Pretty good meditation today", sit_rating=4)

        db.session.add(s)
        db.session.commit()

        self.assertEqual(len(self.u.sit), 1)
        self.assertEqual(self.u.sit[0].sit_title, "Test Sit 1")