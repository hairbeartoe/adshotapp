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
# create the class that will separate the lists
# into 3 different lists to be used for capturing
class db_Query:
    def __init__(self):
        self.pl20 = []
        self.pl60 = []
        self.pl1440 = []
        db_pages = Page.query.all()
        for page in db_pages:
            if page.capture_rate is 20:  # set the information for the 20 minute list
                # set the mobile information
                if page.mobile_capture:
                    page_data = {'url': page.url, 'rate': page.capture_rate, 'directory': page.directory, 'type': 'Mobile',
                                 'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                                 'width': '508'}
                    self.pl20.append(page_data)

                # Set the desktop information
                page_data = {'url': page.url, 'rate': page.capture_rate, 'directory': page.directory, 'type': 'Desktop',
                             'user_agent': 'desktop', 'width': '1280'}
                self.pl20.append(page_data)

            elif page.capture_rate is 60:
                # set the mobile information
                if page.mobile_capture:
                    page_data = {'url': page.url, 'rate': page.capture_rate, 'directory': page.directory, 'type': 'Mobile',
                                 'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                                 'width': '508'}
                    self.pl60.append(page_data)

                # Set the desktop information
                page_data = {'url': page.url, 'rate': page.capture_rate, 'directory': page.directory, 'type': 'Desktop',
                             'user_agent': 'desktop', 'width': '1280'}
                self.pl60.append(page_data)

            else:
                # set the mobile information
                if page.mobile_capture:
                    page_data = {'url': page.url, 'rate': page.capture_rate, 'directory': page.directory, 'type': 'Mobile',
                                 'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                                 'width': '508'}
                    self.pl1440.append(page_data)

                # Set the desktop information
                page_data = {'url': page.url, 'rate': page.capture_rate, 'directory': page.directory, 'type': 'Desktop',
                             'user_agent': 'desktop', 'width': '1280'}
                self.pl1440.append(page_data)


# This is the function that will create the lists
def query():
    return db_Query()


# This was just a test
def test():
    x = query()
    print(x.pl20)


# function to capture the screenshots from the passed list
def screenshot_engine(pages_list):
    for page in pages_list:
        engine.capture(page)
    return


# the following 3 functions are set to capture each list at
# at the specified intervals. Use these in the schedule to run threaded
def capture_20():
    x = query()
    screenshot_engine(x.pl20)
    return


def capture_60():
    x = query()
    screenshot_engine(x.pl60)
    return


def capture_daily():
    x = query()
    screenshot_engine(x.pl1440)
    return


# function to make threads -> details here http://bit.ly/faq_schedule
def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()


# setting the schedule to run the desired functions
schedule.every(10).minutes.do(run_threaded, query)  # this is to query the database every X minutes
schedule.every(20).minutes.do(run_threaded, capture_20)  # this will get screenshots every 20 minutes
schedule.every(60).minutes.do(run_threaded, capture_60)  # this will get screenshots every 60 minutes
schedule.every(1).day.at("05:00").do(run_threaded, capture_daily)  # this will get screenshots every 24 hours

# runs the scheduled jobs
while True:
    schedule.run_pending()
    time.sleep(1)
