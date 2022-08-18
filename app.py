from flask import Flask, render_template, redirect, flash, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
import flask_sqlalchemy
from models import User, Sit, db, connect_db
from quote import today_quote
from forms import UserAddForm, UserLoginForm, NewSitForm, UserEditForm, EditSitForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, create_engine
import os

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

uri = os.environ.get('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://")
engine = create_engine(uri, echo=True)
app.config['SQLALCHEMY_DATABASE_URI'] = (uri, 'postgresql:///sit_db')
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'izsekret')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
toolbar = DebugToolbarExtension(app)

@app.route("/")
def show_homepage():
    
    if g.user:
        user = g.user
        return render_template("index.html", today_quote=today_quote[0]['h'], user=user)
    else:
        return render_template("anon.html", today_quote=today_quote[0]['h'])

@app.route("/admin")
def show_admin_page():
    
    if g.user:
        g.user = User.query.get_or_404(session[CURR_USER_KEY])
        if g.user.is_admin==True:
            user = g.user
            users = User.query.order_by(User.id).all()
            sits = Sit.query.all()
            return render_template("admin.html", users=users, sits=sits, user=user)
        else:
            flash("You do not have admin access", "alert-danger")
            return redirect('/')
    else:
        abort(404)



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
    user=g.user
    do_logout()
    flash(f"{user.username}, you have successfully logged out", "alert-success")
    return redirect('/')

@app.route('/timer')
def show_sit_timer():
    user = g.user
    return render_template('/timer.html', user=user)

@app.route('/sit', methods=['GET', 'POST'])
def show_and_handle_new_sit():
    user = g.user
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
        return render_template('sit.html', form=form, user=user)

@app.route('/users/<int:user_id>/history')
def show_user_sit_history(user_id):
    user = g.user
    sits = Sit.query.filter_by(user_id=user.id).order_by(desc(Sit.timestamp)).all()
    return render_template('/users/history.html', user=user, sits=sits)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user_account(user_id):
    if not g.user:
        flash("Access unauthorized", "alert-danger")
        return redirect('/')
    
    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data

            db.session.commit()
            return redirect(f"/users/{user_id}/history")
        flash("Incorrect password; please try again", 'alert-danger')

    return render_template('users/edit.html', form=form, user_id=user.id, user=user)

@app.route('/users/<int:user_id>/sit/<int:sit_id>', methods=['GET', 'POST'])
def edit_individual_sit_entry(user_id, sit_id):
    if not g.user:
        flash("Access unauthorized", "alert-danger")
        return redirect('/')
    
    user = g.user
    sit = Sit.query.get_or_404(sit_id)
    form = EditSitForm(obj=sit)
    

    if form.validate_on_submit():

        sit.timestamp = form.datetime.data
        sit.sit_title = form.title.data
        sit.duration = form.duration.data
        sit.sit_body = form.body.data
        sit.sit_rating = form.rating.data
        db.session.commit()
        
        return redirect(f'/users/{user_id}/history')

    else:
        return render_template('users/edit_sit.html', user=user, sit=sit, form=form)

@app.route('/users/<int:user_id>/sit/<int:sit_id>/delete', methods=['POST'])
def delete_individual_sit_entry(user_id, sit_id):
    sit = Sit.query.get_or_404(sit_id)
    db.session.delete(sit)
    db.session.commit()
    return redirect(f'/users/{user_id}/history')

@app.route('/tips')
def show_sit_tips_page():
    user = g.user
    return render_template('tips.html', user=user)

@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404