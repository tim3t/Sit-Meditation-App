from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
import flask_sqlalchemy
from models import User, Sit, db, connect_db
from quote import today_quote

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sit_db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'izsekret'

connect_db(app)
toolbar = DebugToolbarExtension(app)

@app.route("/")
def show_homepage():
    return render_template("index.html", today_quote=today_quote)