from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
page = Table('page', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('site', Integer),
    Column('name', String(length=64)),
    Column('url', String(length=64)),
    Column('capture_rate', Integer),
    Column('status', String(length=64)),
    Column('mobile_capture', Boolean),
    Column('date_added', DateTime),
    Column('last_screenshot', DateTime),
    Column('cover_image_path', String(length=140)),
    Column('directory', String(length=140)),
)

image = Table('image', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=140)),
    Column('path', String(length=140)),
    Column('date', DateTime),
    Column('directory', String(length=140)),
    Column('website', Integer),
    Column('page', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['page'].create()
    post_meta.tables['image'].columns['page'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['page'].drop()
    post_meta.tables['image'].columns['page'].drop()
