from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
site = Table('site', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('domain', VARCHAR(length=64)),
    Column('article_page_capture', BOOLEAN),
    Column('capture_rate', INTEGER),
    Column('mobile_capture', BOOLEAN),
    Column('date_added', TIMESTAMP),
    Column('last_screenshot', TIMESTAMP),
    Column('Status', VARCHAR(length=64)),
)

site = Table('site', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('domain', String(length=64)),
    Column('capture_rate', Integer),
    Column('status', String(length=64)),
    Column('mobile_capture', Boolean),
    Column('article_page_capture', Boolean),
    Column('date_added', DateTime),
    Column('last_screenshot', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['site'].columns['Status'].drop()
    post_meta.tables['site'].columns['status'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['site'].columns['Status'].create()
    post_meta.tables['site'].columns['status'].drop()
