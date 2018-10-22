from sqlalchemy import *
from migrate import *
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, BYTEA

from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
apscheduler_jobs = Table('apscheduler_jobs', pre_meta,
    Column('id', VARCHAR(length=191), primary_key=True, nullable=False),
    Column('next_run_time', DOUBLE_PRECISION(precision=53)),
    Column('job_state', BYTEA, nullable=False),
)

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
    Column('aps_jobID', String(length=140)),
    Column('aps_jobID_mobile', String(length=140)),
    Column('track_class', Boolean),
    Column('css_class', String(length=140)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['apscheduler_jobs'].drop()
    post_meta.tables['page'].columns['css_class'].create()
    post_meta.tables['page'].columns['track_class'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['apscheduler_jobs'].create()
    post_meta.tables['page'].columns['css_class'].drop()
    post_meta.tables['page'].columns['track_class'].drop()
