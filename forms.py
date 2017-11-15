from flask import Flask
from app import app,db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, HiddenField
from wtforms.validators import InputRequired, Email, Length, URL
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


STATE_ABBREV = [
  ('AL', 'Alabama'),
  ('AK', 'Alaska'),
  ('AZ', 'Arizona'),
  ('AR', 'Arkansas'),
  ('CA', 'California'),
  ('CO', 'Colorado'),
  ('CT', 'Connecticut'),
  ('DE', 'Delaware'),
  ('DC', 'District of Columbia'),
  ('FL', 'Florida'),
  ('GA', 'Georgia'),
  ('HI', 'Hawaii'),
  ('ID', 'Idaho'),
  ('IL', 'Illinois'),
  ('IN', 'Indiana'),
  ('IA', 'Iowa'),
  ('KS', 'Kansas'),
  ('KY', 'Kentucky'),
  ('LA', 'Louisiana'),
  ('ME', 'Maine'),
  ('MD', 'Maryland'),
  ('MA', 'Massachusetts'),
  ('MI', 'Michigan'),
  ('MN', 'Minnesota'),
  ('MS', 'Mississippi'),
  ('MO', 'Missouri'),
  ('MT', 'Montana'),
  ('NE', 'Nebraska'),
  ('NV', 'Nevada'),
  ('NH', 'New Hampshire'),
  ('NJ', 'New Jersey'),
  ('NM', 'New Mexico'),
  ('NY', 'New York'),
  ('NC', 'North Carolina'),
  ('ND', 'North Dakota'),
  ('OH', 'Ohio'),
  ('OK', 'Oklahoma'),
  ('OR', 'Oregon'),
  ('PA', 'Pennsylvania'),
  ('RI', 'Rhode Island'),
  ('SC', 'South Carolina'),
  ('SD', 'South Dakota'),
  ('TN', 'Tennessee'),
  ('TX', 'Texas'),
  ('UT', 'Utah'),
  ('VT', 'Vermont'),
  ('VA', 'Virginia'),
  ('WA', 'Washington'),
  ('WV', 'West Virginia'),
  ('WI', 'Wisconsin'),
  ('WY', 'Wyoming'),
]

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[InputRequired(), Length(min=4, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    email = StringField('Email')
    team_name = StringField('Team')
    username = StringField('Name')
    password = PasswordField('Password')
    remember = BooleanField('Remember me')

class AddUserForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Please enter a valid email'), Length(max=50)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=50)])


class AddSiteForm(FlaskForm):
    domain_name = StringField(validators=[InputRequired()])
    rate = SelectField(choices=[ ('1440', 'Once daily'), ('60', 'Once every hour'), ( '30', 'Once every 30 minutes'), ('15', 'Once every 15 minutes')])
    article = BooleanField(default=False)
    mobile = BooleanField(default=False)
    amount = StringField()
    stripeToken = HiddenField()
    stripeEmail = HiddenField()


class FindTeamForm(FlaskForm):
    email = StringField(validators=[InputRequired()])

class CreateCollectionForm(FlaskForm):
    name = StringField(validators=[InputRequired()])
    image = HiddenField()


class EditUserProfile(FlaskForm):
    email = StringField('Email Address', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[Length(min=2, max=25)])
    street_address = StringField('Street Address', validators=[Length(min=2, max=40)])
    city = StringField('City', validators=[Length(min=2, max=30)])
    state = SelectField(choices=STATE_ABBREV)
    postal_code = StringField('Postal Code', validators=[Length(min=2, max=9)])


class AddImagetoCollection(FlaskForm):
    image_id = StringField('Image', validators=[InputRequired()])
    colllection = StringField('Collection', validators=[InputRequired()])
