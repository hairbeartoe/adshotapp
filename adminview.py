from flask import Flask
from app import db, models
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


adminpage = Admin(app)
adminpage.add_view(ModelView(User, db.session))