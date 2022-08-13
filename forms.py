from ast import Num
from tokenize import Number
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, EmailField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, Length

class UserAddForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])

class UserEditForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])

class UserLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])

class NewSitForm(FlaskForm):
    datetime = DateField('Sit Date', validators=[DataRequired()], format='%Y-%m-%d')
    duration = IntegerField('Duration (in minutes)', validators=[DataRequired(), NumberRange(min=1)])
    title = StringField('Title or Topic', validators=[DataRequired()])
    body = TextAreaField('Sit Notes', validators=[DataRequired()])
    rating = SelectField('Rating', validators=[DataRequired()], choices=[(5,'Great'),(4, 'Good'),(3,'Okay'),(2,'Fair'),(1,'Poor')])

class EditSitForm(FlaskForm):
    datetime = DateField('Sit Date', validators=[DataRequired()], format='%Y-%m-%d')
    duration = IntegerField('Duration (in minutes)', validators=[DataRequired(), NumberRange(min=1)])
    title = StringField('Title or Topic', validators=[DataRequired()])
    body = TextAreaField('Sit Notes', validators=[DataRequired()])
    rating = SelectField('Rating', validators=[DataRequired()], choices=[(5,'Great'),(4, 'Good'),(3,'Okay'),(2,'Fair'),(1,'Poor')])