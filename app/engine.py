#!/usr/bin/python
import hmac
from hashlib import sha1
import urllib
from urllib import parse,request
import datetime
import os
from app import db
from app.models import User,Site, Image, subscriptions, Team, Collection, Page




def screenshot_engine(query):

    # set the arguments
    def dict_items(query):
        # TODO
        args = {'url': query.get('url'),
                'delay': 15,
                'width': query.get('width'),
                'user_agent': query.get('user_agent'),
                'force': True,
                'full_page': True}
        return args


    # Pass the json arguments into the URLBOX class
    def urlbox(args):
        apiKey = "mMb16EovKVO0Oakc"
        apiSecret = "072aac879ad646719e06a8d48a5c1c43"
        queryString = urllib.parse.urlencode(args,True)
        #hmacToken = hmac.new(apiSecret, queryString, sha1)
        #token = hmacToken.digest().encode('hex')
        return "https://api.urlbox.io/v1/%s/png?%s" % (apiKey, queryString)

    # Using the url returned by urlbox class, download image and save into location
    def download_image(url, imageName, directory):
        if os.path.isdir(directory):
            os.chdir(directory)
            urllib.request.urlretrieve(url, imageName)
            print('image saved to ' + os.getcwd() + ' - ' +imageName)
            os.chdir('../../../../')
        else:
            os.mkdir(directory)
            os.chdir(directory)
            urllib.request.urlretrieve(url, imageName)
            print('image saved to ' + os.getcwd() + ' - ' +imageName)
            os.chdir('../../../../')
        return

    def add_db_record(query, imageName, file_path):
        page = Page.query.filter_by(url=query.get('url')).first()
        site = Site.query.filter_by(id=page.site).first()
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_image = Image(name=imageName,
                          date=date,
                          pages=page,
                          images=site,
                          device=query.get('type'),
                          path=file_path)
        page.last_screenshot = date
        site.last_screenshot = date
        db.session.add(new_image)
        db.session.commit()

    def remove_prefix(text, prefix):
        if text.startswith(prefix):
            return text[len(prefix):]
        return text

    args = dict_items(query)
    url = (urlbox(args))
    name = datetime.datetime.now().strftime("%I:%M %p") +'-' + query.get('type') + '.png'
    directory = query.get('directory')
    print('getting image...')
    download_image(url, name, directory)
    file_path = remove_prefix(directory,'static/images') + "/" +name
    #print(file_path)
    add_db_record(query, name, file_path)

# Test run
# screenshot_engine(query)
