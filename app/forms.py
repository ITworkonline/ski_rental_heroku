from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError

from app.models import User


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), length(min=5, max=20)])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # check the database
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose another one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already taken. Please choose another one')


# login form from wtf
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), length(min=5, max=20)])
    remember = BooleanField('Remember')
    submit = SubmitField('Sign in')


# manager page check the password
class ManagerForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), length(min=5, max=20)])
    submit = SubmitField('check')


# ski form from wtf
class SkiForm(FlaskForm):
    ski_brand = SelectField('ski_brand', choices=[('Nordia', 'Nordia'), ('Blizzard', 'Blizzard'),
                                                  ('Atomic', 'Atomic'), ('Rossignol', 'Rossignol'),
                                                  ('Elan', 'Elan'), ('Santa', 'Santa'), ('Black Crows', 'Black Crows')])
    ski_type = SelectField('ski_type', choices=[('Skis', 'Skis'), ('Snowboard', 'Snowboard'),
                                                  ('Poles', 'Poles'), ('Ski Boots', 'Ski Boots'),
                                                  ('Ski Helmet', 'Ski Helmet'), ('Gloves', 'Gloves'),
                                                  ('Goggles', 'Goggles'), ('Ski Jacket', 'Ski Jacket'),
                                                  ('Ski Pants', 'Ski Pants'), ('Backpack', 'Backpack')])
    price = IntegerField('price', validators=[DataRequired()])
    submit = SubmitField('add in')


# ski edit form from wtf
class EditForm(FlaskForm):
    ski_brand = SelectField('ski_brand', choices=[('Nordia', 'Nordia'), ('Blizzard', 'Blizzard'),
                                                  ('Atomic', 'Atomic'), ('Rossignol', 'Rossignol'),
                                                  ('Elan', 'Elan'), ('Santa', 'Santa'), ('Black Crows', 'Black Crows')])
    ski_type = SelectField('ski_type', choices=[('Skis', 'Skis'), ('Snowboard', 'Snowboard'),
                                                  ('Poles', 'Poles'), ('Ski Boots', 'Ski Boots'),
                                                  ('Ski Helmet', 'Ski Helmet'), ('Gloves', 'Gloves'),
                                                  ('Goggles', 'Goggles'), ('Ski Jacket', 'Ski Jacket'),
                                                  ('Ski Pants', 'Ski Pants'), ('Backpack', 'Backpack')])
    price = IntegerField('price', validators=[DataRequired()])
    availability = StringField('availability (if return, enter "Yes")', validators=[DataRequired(), length(min=1, max=255)])
    submit = SubmitField('update ')
