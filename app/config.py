import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/adshotapp'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SECRET_KEY = 'EchoDog'

IMAGES_PATH=['static/images']

MAIL_SERVER='smtp.gmail.com'
MAIL_USERNAME='getupliftedsite@gmail.com'
MAIL_PASSWORD='Bamb00zl3'
MAIL_PORT='465'
MAIL_USE_SSL=True
MAIL_USE_TLS=False