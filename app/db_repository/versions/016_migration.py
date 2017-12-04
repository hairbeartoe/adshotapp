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
    Column('team', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['city'].create()
    post_meta.tables['user'].columns['first_name'].create()
    post_meta.tables['user'].columns['last_name'].create()
    post_meta.tables['user'].columns['postal_code'].create()
    post_meta.tables['user'].columns['state'].create()
    post_meta.tables['user'].columns['street_address'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['city'].drop()
    post_meta.tables['user'].columns['first_name'].drop()
    post_meta.tables['user'].columns['last_name'].drop()
    post_meta.tables['user'].columns['postal_code'].drop()
    post_meta.tables['user'].columns['state'].drop()
    post_meta.tables['user'].columns['street_address'].drop()
