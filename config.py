DEBUG = True

# Define the application directory
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# Postgres
SQLALCHEMY_DATABASE_URI = 'postgresql://hflores:tocksTeler@localhost/adshotapp'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SECRET_KEY = 'EchoDog'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Define the images path to serve images
IMAGES_PATH=['static/images']

# Define the mail settings to send mail from the app
MAIL_SERVER='smtp.gmail.com'
MAIL_USERNAME='Pagesnapsite@gmail.com'
MAIL_PASSWORD='zqddqpxaujmsjacu'
MAIL_PORT='587'
MAIL_USE_SSL=False
MAIL_USE_TLS=True

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "EchoDog"

# Secret key for signing cookies
SECRET_KEY = "EchoDog"
