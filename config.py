# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# Postgres
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/adshotapp'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SECRET_KEY = 'EchoDog'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Define the images path to serve images
IMAGES_PATH=['static/images']

# Define the mail settings to send mail from the app
MAIL_SERVER='smtp.gmail.com'
MAIL_USERNAME='getupliftedsite@gmail.com'
MAIL_PASSWORD='Bamb00zl3'
MAIL_PORT='465'
MAIL_USE_SSL=True
MAIL_USE_TLS=False

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "EchoDog"

# Secret key for signing cookies
SECRET_KEY = "EchoDog"