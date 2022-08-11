"""Seed file to generate sample users for Sit Meditation app"""

from unicodedata import ucd_3_2_0
from models import User, Sit, db 
from app import app

db.drop_all()
db.create_all()

u1 = User(username='Jones1', password='Test123', first_name="Matthew", last_name="Jones", email="mattjones@listmail.com")
u2 = User(username='Smith2', password='Test1234', first_name="Alicia", last_name="Smith", email="alicia.smith@coldmail.net")
u3 = User(username='Vaughn3', password='Test12345', first_name="Craig", last_name="Vaughn", email="craiggery@speednet.org")
u4 = User(username='Richards4', password='Test123456', first_name="Kimberly", last_name="Richards", email="kim_richards@nsa.gov")

db.session.add_all([u1, u2, u3, u4])
db.session.commit()

