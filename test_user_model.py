import os
from unittest import TestCase
from sqlalchemy import exc
from models import User, Sit, db 

os.environ['DATABASE_URL'] = "postgresql:///sit_db_test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "password", "chester", "tester", "test1@email.com")
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup("test2", "password", "esther", "tester", "test2@email.com")
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        u = User(username="BillyBoy", password="HASHED_PASSWORD", first_name="Billy", last_name="Boy", email="billyboy@email.com")

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.sit), 0)

    def test_valid_signup(self):
        u_test = User.signup("KittyGirl", "password", "Kitty", "Girl", "kittygirl@email.com")
        uid = 99999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "KittyGirl")
        self.assertNotEqual(u_test.password, "password")
        self.assertEqual(u_test.first_name, "Kitty")
        self.assertEqual(u_test.last_name, "Girl")
        self.assertEqual(u_test.email, "kittygirl@email.com")
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username(self):
        invalid = User.signup(None, "password", "Sammy", "Smiles", "sammysmiles@email.com")
        uid = 12345
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))
