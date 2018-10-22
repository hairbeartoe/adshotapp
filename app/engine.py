#!/usr/bin/python
import hmac
from hashlib import sha1
import urllib
from urllib import parse, request
import datetime
import os
from app import db
from app.models import User, Site, Image, subscriptions, Team, Collection, Page
from random import randint
from apscheduler.schedulers.background import BackgroundScheduler
from app import app
from bs4 import BeautifulSoup
import requests
import re

time_delay = randint(15000, 26000)


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
    delay = randint(18000, 26000)
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
    delay = randint(15000, 26000)
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
def add_db_record(id, file_params):
    page = Page.query.filter_by(id=id).first()
    site = Site.query.filter_by(id=page.site).first()
    date = file_params.get('capture_date')
    new_image = Image(name=file_params.get('name'),
                      date=date,
                      pages=page,
                      images=site,
                      isDeleted=False,
                      device=file_params.get('type'),
                      path=file_params.get('file_path'))
    if page.cover_image_path is None:
        page.cover_image_path = new_image.path
    if site.cover_image_path is None:
        site.cover_image_path = new_image.path
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


def gen_url(url, width, type):
    url = url
    width = width
    agent_options = {'Desktop': 'desktop',
                     'Mobile': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
    user_agent = agent_options.get(type)
    delay = randint(18000, 26000)
    force = True
    full_page = True
    scroll = True
    url_args = {'url': url, 'delay': delay, 'width': width, 'user_agent': user_agent, 'force': force,
                'full_page': full_page, 'scroll': scroll}
    query_string = urllib.parse.urlencode(url_args, True)
    capture_url = "http://138.197.201.156:5000/png?%s" % (query_string)
    # print(capture_url)
    return capture_url


def set_file_params2(url, width, type, directory):
    url = url
    width = width
    agent_options = {'Desktop': 'desktop', 'Mobile': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
    user_agent = agent_options.get(type)
    type = type
    delay = randint(15000, 26000)
    force = True
    full_page = True
    directory = directory
    capture_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    capture_url = 'abc'
    name = datetime.datetime.now().strftime("%I:%M %p") + '-' + type + '.png'
    date_folder = datetime.datetime.now().strftime("%m-%d-%Y")
    file_path = remove_prefix(directory, 'static/images') + "/" + date_folder + "/" + name
    file_args = {'url': url, 'delay': delay, 'width': width, 'force': force,
                 'capture_date': capture_date, 'full_page': full_page, 'type': type, 'directory': directory,
                 'name': name, 'file_path': file_path, 'capture_url': capture_url}
    return file_args


def capture2(page_id, width, type):
    with app.app_context():
        page = Page.query.filter_by(id=page_id).first()  # this is a query to gather all info for this capture
        # print('page found')
        capture_url = gen_url(page.url, width, type)
        # print('url generated')
        file_parameters = set_file_params2(page.url, width, type, page.directory)
        # print('parameters set')
        file_parameters['capture_url'] = capture_url
        download_image(file_parameters)
        # print('downloaded image')
        add_db_record(page.id, file_parameters)
        # print('added to DB')


def capture3(page_id, width, type, css_class):
    with app.app_context():
        page = Page.query.filter_by(id=page_id).first()  # this is a query to gather all info for this capture
        css_class = css_class
        base_page = requests.get(page.url)
        soup = BeautifulSoup(base_page.text, features="html.parser")
        first_class = soup.find(class_=css_class)
        a_tag = first_class.attrs['href']
        download_url = a_tag
        # print(download_url)
        capture_url = gen_url(download_url, width, type)
        file_parameters = set_file_params2(download_url, width, type, page.directory)
        file_parameters['capture_url'] = capture_url
        download_image(file_parameters)
        add_db_record(page.id, file_parameters)



