from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
site = Table('site', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('domain', VARCHAR(length=64)),
    Column('capture_rate', INTEGER),
    Column('status', VARCHAR(length=64)),
    Column('mobile_capture', BOOLEAN),
    Column('article_page_capture', BOOLEAN),
    Column('date_added', TIMESTAMP),
    Column('last_screenshot', TIMESTAMP),
    Column('cover_image_path', VARCHAR(length=140)),
    Column('directory', VARCHAR(length=140)),
    Column('url', VARCHAR(length=64)),
)

image = Table('image', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=140)),
    Column('path', String(length=140)),
    Column('date', DateTime),
    Column('directory', String(length=140)),
    Column('device', String(length=20)),
    Column('website', Integer),
    Column('page', Integer),
    Column('isDeleted', Boolean),
    Column('isSaved', Boolean),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('nickname', VARCHAR(length=64)),
    Column('first_name', VARCHAR(length=64)),
    Column('last_name', VARCHAR(length=64)),
    Column('street_address', VARCHAR(length=64)),
    Column('city', VARCHAR(length=64)),
    Column('state', VARCHAR(length=64)),
    Column('postal_code', VARCHAR(length=9)),
    Column('email', VARCHAR(length=120)),
    Column('password', VARCHAR(length=80)),
    Column('profile', VARCHAR(length=80)),
    Column('status', VARCHAR(length=80)),
    Column('last_login', TIMESTAMP),
    Column('date_joined', TIMESTAMP),
    Column('collection_count', INTEGER),
    Column('confirmed_email', BOOLEAN),
    Column('team', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['site'].columns['article_page_capture'].drop()
    pre_meta.tables['site'].columns['capture_rate'].drop()
    pre_meta.tables['site'].columns['url'].drop()
    post_meta.tables['image'].columns['isDeleted'].create()
    post_meta.tables['image'].columns['isSaved'].create()
    pre_meta.tables['user'].columns['city'].drop()
    pre_meta.tables['user'].columns['postal_code'].drop()
    pre_meta.tables['user'].columns['state'].drop()
    pre_meta.tables['user'].columns['street_address'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['site'].columns['article_page_capture'].create()
    pre_meta.tables['site'].columns['capture_rate'].create()
    pre_meta.tables['site'].columns['url'].create()
    post_meta.tables['image'].columns['isDeleted'].drop()
    post_meta.tables['image'].columns['isSaved'].drop()
    pre_meta.tables['user'].columns['city'].create()
    pre_meta.tables['user'].columns['postal_code'].create()
    pre_meta.tables['user'].columns['state'].create()
    pre_meta.tables['user'].columns['street_address'].create()
