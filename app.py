from flask import Flask, render_template, redirect, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
import flask_sqlalchemy
from models import User, Sit, db, connect_db
from quote import today_quote
from forms import UserAddForm, UserLoginForm, NewSitForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sit_db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'izsekret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
toolbar = DebugToolbarExtension(app)

@app.route("/")
def show_homepage():

    if g.user:
        return render_template("index.html", today_quote=today_quote[0]['h'])
    else:
        return render_template("anon.html", today_quote=today_quote[0]['h'])

@app.route("/admin")
def show_admin_page():
    g.user = User.query.get(session[CURR_USER_KEY])
    if g.user.is_admin==True:
        users = User.query.order_by(User.id).all()
        sits = Sit.query.all()
        return render_template("admin.html", users=users, sits=sits)
    else:
        flash("You do not have admin access", "alert-danger")
        return redirect('/')

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

@app.route('/signup', methods=['GET', 'POST'])
def show_and_handle_signup_form():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        try: 
            user = User.signup(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, username=form.username.data, password=form.password.data)
            db.session.commit()
        except IntegrityError as e:
            flash("Username already taken", "alert-danger")
            return render_template('signup.html', form=form)

        do_login(user)
        flash(f"Welcome to Sit Meditation, {user.username}!", "alert-success")
        return redirect('/')
    
    else:
        return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def show_login_form():

    form = UserLoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        
        if user:
            do_login(user)
            flash(f"Welcome back, {user.username}!", "alert-success")
            return redirect('/')
        flash("Invalid credentials.  Please check username and password and try again", "alert-danger")
    
    return render_template('login.html', form=form)

@app.route('/logout')
def user_logout():
    do_logout()
    flash("You have successfully logged out", "alert-success")
    return redirect('/')

@app.route('/sit', methods=['GET', 'POST'])
def show_and_handle_new_sit():

    form = NewSitForm()
    if form.validate_on_submit():
        user_id = g.user.id
        timestamp = form.datetime.data
        duration = form.duration.data
        sit_title = form.title.data
        sit_body = form.body.data
        sit_rating = form.rating.data

        sit = Sit(user_id=user_id, timestamp=timestamp, duration=duration, sit_title=sit_title, sit_body=sit_body, sit_rating=sit_rating)
        db.session.add(sit)
        db.session.commit()
        flash(f"Successfully created new Sit for {timestamp}", "alert-success")
        return redirect(f'/users/{user_id}/history')
    else:
        return render_template('sit.html', form=form)

@app.route('/users/<int:user_id>/history')
def show_user_sit_history(user_id):
    user = g.user
    sits = Sit.query.filter_by(user_id=user.id).order_by(desc(Sit.timestamp)).all()
    return render_template('/users/history.html', user=user, sits=sits)

@app.route('/users/<int:user_id>/sit/<int:sit_id>', methods=['GET', 'POST'])
def edit_individual_sit_entry(user_id, sit_id):
    user = g.user
    sit = Sit.query.get_or_404(sit_id)
    form = NewSitForm()
    form.datetime.data = sit.timestamp
    form.title.data = sit.sit_title
    form.duration.data = sit.duration
    form.body.data = sit.sit_body
    form.rating.data = sit.sit_rating

    if form.validate_on_submit():

        sit.timestamp = form.datetime.data
        sit.sit_title = form.title.data
        sit.duration = form.duration.data
        sit.sit_body = form.body.data
        sit.sit_rating = form.rating.data
        db.session.commit()
        
        return redirect(f'/users/{user_id}/history.html')

    else:
        return render_template('users/sitentry.html', user=user, sit=sit, form=form)

@app.route('/users/<int:user_id>/sit/<int:sit_id>/delete', methods=['POST'])
def delete_individual_sit_entry(user_id, sit_id):
    sit = Sit.query.get_or_404(sit_id)
    db.session.delete(sit)
    db.session.commit()
    return redirect(f'/users/{user_id}/history')

@app.route('/tips')
def show_sit_tips_page():
    return render_template('tips.html')