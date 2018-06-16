from app import app, db, engine
from app.models import User, Site, Image, subscriptions, Team, Collection, Page
from datetime import datetime
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import schedule
import threading
import time
import app.engine


# function to gather what's needed to take a screenshot automatically
# set an empty list that will be the container for the pages
# Query the db for all pages
# Create a dictionary with all needed info for each page
# Add each dictionary to the empty pages list (a list of dictionary's)
def query_db():
    pages_list = []
    db_pages = Page.query.all()
    for page in db_pages:

        # set the mobile information
        if page.mobile_capture:
            page_data = {'url': page.url, 'rate': page.capture_rate, 'directory': page.directory, 'type': 'Mobile',
                'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                         'width': '508'}
            pages_list.append(page_data)

        # Set the desktop information
        page_data = {'url': page.url, 'rate': page.capture_rate, 'directory': page.directory, 'type': 'Desktop',
                     'user_agent': 'desktop', 'width': '1280'}
        pages_list.append(page_data)
    return pages_list


# function to auto-run the screenshots
def screenshot_engine():
    pages_list = query_db()
    for page in pages_list:
        engine.capture(page)


# function to make threads -> details here http://bit.ly/faq_schedule
def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()


# setting the schedule to run the screenshot engine function
schedule.every(5).minutes.do(screenshot_engine)

# runs the scheduled jobs
while True:
    schedule.run_pending()
    time.sleep(1)
