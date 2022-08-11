from flask import Flask, render_template, redirect, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
import flask_sqlalchemy
from models import User, Sit, db, connect_db
from quote import today_quote

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sit_db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'izsekret'

connect_db(app)
toolbar = DebugToolbarExtension(app)

@app.route("/")
def show_homepage():

    if g.user:
        return render_template("index.html", today_quote=today_quote)
    else:
        return render_template("anon.html", today_quote=today_quote)

@app.route("/admin")
def show_admin_page():
    users = User.query.all()
    return render_template("admin.html", users=users)

@app.before_request
def add_user_to_g():
    """When logged in, add curr_user to global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    session[CURR_USER_KEY] = user.id

def do_logout():

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup')
def show_signup_form():
    return render_template('signup.html')

@app.route('/login')
def show_login_form():
    return render_template('login.html')