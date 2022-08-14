"""Seed file to generate sample users for Sit Meditation app"""

from unicodedata import ucd_3_2_0
from models import User, Sit, db 
from app import app

db.drop_all()
db.create_all()

u1 = User.signup(username='Jones1', password='Jones123', first_name="Matthew", last_name="Jones", email="mattjones@listmail.com")
u2 = User.signup(username='Smith2', password='Smith123', first_name="Alicia", last_name="Smith", email="alicia.smith@coldmail.net")
u3 = User.signup(username='Vaughn3', password='Vaughn123', first_name="Craig", last_name="Vaughn", email="craiggery@speednet.org")
u4 = User.signup(username='Richards4', password='Richards123', first_name="Kimberly", last_name="Richards", email="kim_richards@nsa.gov")
a1 = User.signup(username="Admin", password="Admin123", first_name="Admin", last_name="Account", email="admin@email.com")


db.session.add_all([u1, u2, u3, u4, a1])
db.session.commit()

