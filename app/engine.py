#!/usr/bin/python
import hmac
from hashlib import sha1
import urllib
from urllib import parse, request
import datetime
import os
from app import db
from app.models import User, Site, Image, subscriptions, Team, Collection, Page


# util for making the name work by removing un-needed prefix
def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


# set parameters needed to generate the url for downloading the image
def set_url_params(query):
    url = query.get('url')
    width = query.get('width')
    user_agent = query.get('user_agent')
    delay = 5000
    force = True
    full_page = True
    scroll = True
    url_args = {'url': url, 'delay': delay, 'width': width, 'user_agent': user_agent, 'force': force,
                'full_page': full_page, 'scroll': scroll}
    return url_args


# set the parameters needed to handle any transactions with the database
def set_file_params(query):
    url = query.get('url')
    width = query.get('width')
    user_agent = query.get('user_agent')
    type = query.get('type')
    delay = 15
    force = True
    full_page = True
    directory = query.get('directory')
    capture_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    capture_url = 'abc'
    name = datetime.datetime.now().strftime("%I:%M %p") + '-' + query.get('type') + '.png'
    date_folder = datetime.datetime.now().strftime("%m-%d-%Y")
    file_path = remove_prefix(directory, 'static/images') + "/" + date_folder + "/" + name
    file_args = {'url': url, 'delay': delay, 'width': width, 'user_agent': user_agent, 'force': force,
                 'capture_date': capture_date, 'full_page': full_page, 'type': type, 'directory': directory,
                 'name': name, 'file_path': file_path, 'capture_url': capture_url}
    return file_args


# Pass the json arguments into the generate url class
def generate_url(args):
    api_key = "vB6MvLUCmPp31An8"
    api_secret = "072aac879ad646719e06a8d48a5c1c43"
    query_string = urllib.parse.urlencode(args, True)
    # hmacToken = hmac.new(apiSecret, queryString, sha1)
    # token = hmacToken.digest().encode('hex')
    capture_url = "http://138.197.201.156:5000/png?%s" % (query_string)
    # capture_url = "https://api.urlbox.io/v1/%s/png?%s" % (api_key, query_string)
    return capture_url


# Using the url returned by generate capture url class, download image and save into proper location
def download_image(file_params):
    # Set the variables
    date_folder = datetime.datetime.now().strftime("%m-%d-%Y")
    file = os.path.join('app', file_params.get('directory'), date_folder, file_params.get('name'))
    file_dir = os.path.join('app', file_params.get('directory'), date_folder)
    url = file_params.get('capture_url')
    # If the directory to save the image exists change working directory to save location, download image, and return
    # else, make the new directory to save the image, download the image there, and return to main working directory
    if os.path.exists(file_dir):
        urllib.request.urlretrieve(url, file)
    else:
        os.makedirs(file_dir, exist_ok=True)
        urllib.request.urlretrieve(url, file)
    return


# add a record with the image to the database so the new image can be viewed
def add_db_record(query, file_params):
    page = Page.query.filter_by(url=query.get('url')).first()
    site = Site.query.filter_by(id=page.site).first()
    date = file_params.get('capture_date')
    new_image = Image(name=file_params.get('name'),
                      date=date,
                      pages=page,
                      images=site,
                      device=file_params.get('type'),
                      path=file_params.get('file_path'))
    page.last_screenshot = date
    site.last_screenshot = date
    db.session.add(new_image)
    db.session.commit()


# capture class that handles all functions to download the image to the correct location
def capture(query):
    url_params = set_url_params(query)
    file_params = set_file_params(query)
    capture_url = generate_url(url_params)
    file_params['capture_url'] = capture_url
    download_image(file_params)
    add_db_record(query, file_params)
