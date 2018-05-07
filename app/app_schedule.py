from app import app, db, engine
from app.models import User, Site, Image, subscriptions, Team, Collection, Page
from datetime import datetime
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import schedule
import threading
import time
from app.engine import screenshot_engine

pages = Page.query.all()
list =[]

for page in pages:
    if page.mobile_capture:
        data = {
            'url': page.url,
            'rate': page.capture_rate,
            'directory': page.directory,
            'type': 'Mobile',
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'width': '508'
        }
        list.append(data)

    data = {
        'url': page.url,
        'rate': page.capture_rate,
        'directory': page.directory,
        'type': 'Desktop',
        'user_agent': 'desktop',
        'width': '1280'
    }
    list.append(data)

#print(list[4])


def job_1():
    for item in list:
        screenshot_engine(item)
        #print('screenshot captured: ' + item.get('url'))


# function to make threads -> details here http://bit.ly/faq_schedule
def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()


#schedule.every(2).minutes.do(run_threaded,job_1(list))              # like hashtag
#schedule.every(1).days.at("14:00").do(run_threaded, job_1(list))    # like followers of users from file
schedule.every(20).minutes.do(run_threaded, job_1)    # capture images

job_1()

'''
while True:
    schedule.run_pending()
    time.sleep(1)
'''
