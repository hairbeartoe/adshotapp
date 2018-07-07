from app import app, db
from app.models import User, Site, Image, Team, Collection, Page, MyAdminModel, MyAdminIndexView
from app.forms import LoginForm, PasswordResetRequestForm, ChangePasswordForm, RegisterForm,AddSiteForm, EditUserProfile, AddImagetoCollection, CreateCollectionForm, AddUserForm, FindTeamForm,SendCollectionForm, AddPageForm
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from sqlalchemy import Date, cast, desc
from flask_images import resized_img_src, Images
from datetime import datetime
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import stripe
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os.path as op

images = Image.query.all()

for image in images:
    image.isDeleted = False

db.session.commit()