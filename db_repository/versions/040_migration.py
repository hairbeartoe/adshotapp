from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64)),
    Column('first_name', String(length=64)),
    Column('last_name', String(length=64)),
    Column('street_address', String(length=64)),
    Column('city', String(length=64)),
    Column('state', String(length=64)),
    Column('postal_code', String(length=9)),
    Column('email', String(length=120)),
    Column('password', String(length=80)),
    Column('profile', String(length=80)),
    Column('status', String(length=80)),
    Column('last_login', DateTime),
    Column('date_joined', DateTime),
    Column('collection_count', Integer),
    Column('confirmed_email', Boolean),
    Column('team', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['confirmed_email'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['confirmed_email'].drop()
