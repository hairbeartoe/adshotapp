from app import db
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, flash
from flask_admin import AdminIndexView


subscriptions = db.Table('subscriptions',
                         db.Column('id', db.Integer, primary_key=True),
                         db.Column('subscriber_id', db.Integer, db.ForeignKey('team.id')),
                         db.Column('site_id', db.Integer, db.ForeignKey('site.id')))


collections = db.Table('collections',
                         db.Column('id', db.Integer, primary_key=True),
                         db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                         db.Column('collection_id', db.Integer, db.ForeignKey('collection.id')))


image_collections = db.Table('images',
                         db.Column('id', db.Integer, primary_key=True),
                         db.Column('image_id', db.Integer, db.ForeignKey('image.id')),
                         db.Column('collection_id', db.Integer, db.ForeignKey('collection.id')))



#set the user db model and link to sites (many to many relationship)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(80), index=True)
    profile = db.Column(db.String(80), index=True)
    status = db.Column(db.String(80), index=True)
    last_login = db.Column(db.DateTime(), index=True)
    date_joined = db.Column(db.DateTime(), index=True)
    collection_count = db.Column(db.Integer, index=True)
    confirmed_email = db.Column(db.Boolean, index=True)
    team = db.Column(db.Integer, db.ForeignKey('team.id'))
    collections = db.relationship('Collection',
                            secondary=collections,
                            primaryjoin=(collections.c.collection_id == id),
                            #secondaryjoin=(subscriptions.c.site_id == id),
                            backref=db.backref('users', lazy='dynamic'),
                            lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickname)


# set the collections db
class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    cover_image_path = db.Column(db.String(140))
    sent_count = db.Column(db.Integer)
    _users = db.relationship('User', secondary=collections, backref=db.backref('collections_backref', lazy='dynamic'))
    images = db.relationship('Image',
                            secondary = image_collections,
                            primaryjoin=(image_collections.c.collection_id == id),
                            #secondaryjoin=(subscriptions.c.site_id == id),
                            backref=db.backref('Collections', lazy='dynamic'),
                            lazy='dynamic',
                            passive_deletes=True)

    def __repr__(self):
        return '<Collection %r>' % (self.name)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    admin_user = db.relationship('User', backref='admin', lazy='dynamic')
    subscriptions = db.relationship('Site',
                                 secondary=subscriptions,
                                 primaryjoin=(subscriptions.c.subscriber_id == id),
                                 #secondaryjoin=(subscriptions.c.site_id == id),
                                 backref=db.backref('subscribers', lazy='dynamic'),
                                 lazy='dynamic')
    plan = db.Column(db.String(64), index=True)
    pages_available = db.Column(db.Integer)

    def __repr__(self):
        return '<Team %r>' % (self.name)


# set the sites db model
class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(64), index=True)
    images = db.relationship('Image', backref='images', lazy='dynamic')
    pages = db.relationship('Page', backref='sites', lazy='dynamic')
    status = db.Column(db.String(64), index=True)
    mobile_capture = db.Column(db.Boolean)
    date_added = db.Column(db.DateTime, index=True)
    last_screenshot = db.Column(db.DateTime, index=True)
    cover_image_path = db.Column(db.String(140))
    directory = db.Column(db.String(140))


    def __repr__(self):
        return '<Site %r>' % (self.domain)


# set the page db model
class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.Integer, db.ForeignKey('site.id'))
    name = db.Column(db.String(64), index=True)
    url = db.Column(db.String(64), index=True)
    images = db.relationship('Image', backref='pages', lazy='dynamic')
    capture_rate = db.Column(db.Integer)
    status = db.Column(db.String(64), index=True)
    mobile_capture = db.Column(db.Boolean)
    date_added = db.Column(db.DateTime, index=True)
    last_screenshot = db.Column(db.DateTime, index=True)
    cover_image_path = db.Column(db.String(140))
    directory = db.Column(db.String(140))

    def __repr__(self):
        return '<Page %r>' % (self.name)


# set the image db
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    path = db.Column(db.String(140))
    date = db.Column(db.DateTime)
    directory = db.Column(db.String(140))
    device = db.Column(db.String(20))
    website = db.Column(db.Integer, db.ForeignKey('site.id'))
    page = db.Column(db.Integer, db.ForeignKey('page.id'))

    def __repr__(self):
        return '<Image %r>' % (self.name)


''' 
 This is the area that handles the Admin Login Functions
 The AdminIndexView stops users from accessing the Admin Home
 The MyAdminModel is what stops users from accessing the Models
  within the index
'''


class MyAdminModel(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.profile == 'System Administrator':
                return True
            else:
                return False
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        flash('Please login as an Administrator', category='info')
        return redirect(url_for('login'))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.profile == 'System Administrator':
                return True
            else:
                return False
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        flash('Please login as an Administrator', category='info')
        return redirect(url_for('login'))
