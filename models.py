from app import db
from flask_login import UserMixin


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
    street_address = db.Column(db.String(64), index=True)
    city = db.Column(db.String(64), index=True)
    state = db.Column(db.String(64), index=True)
    postal_code = db.Column(db.String(9), index=True)
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

    def __repr__(self):
        return '<Team %r>' % (self.name)


#set the sites db model
class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(64), index=True, unique=True)
    images = db.relationship('Image', backref='images', lazy='dynamic')
    capture_rate = db.Column(db.Integer)
    status = db.Column(db.String(64), index=True)
    mobile_capture = db.Column(db.Boolean)
    article_page_capture = db.Column(db.Boolean)
    date_added = db.Column(db.DateTime, index=True)
    last_screenshot = db.Column(db.DateTime, index=True)


    def __repr__(self):
        return '<Site %r>' % (self.domain)

# set the image db
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    path = db.Column(db.String(140))
    date = db.Column(db.DateTime)
    website = db.Column(db.Integer, db.ForeignKey('site.id'))

    def __repr__(self):
        return '<Image %r>' % (self.date)





