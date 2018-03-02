#!/usr/bin/python
import hmac
from hashlib import sha1
import urllib
from urllib import parse,request
from urllib.request import urlretrieve, urlopen


def urlbox(args):
    apiKey = "mMb16EovKVO0Oakc"
    apiSecret = "072aac879ad646719e06a8d48a5c1c43"
    queryString = urllib.parse.urlencode(args, True)
    #hmacToken = hmac.new(apiSecret, queryString, sha1)
    #token = hmacToken.digest().encode('hex')
    return "https://api.urlbox.io/v1/%s/png?%s" % (apiKey, queryString)


def download_image(url,imageName):
    """
    download an image in the form of
    url = http://www.example.com
    name = '00000000.jpg'
    """
    urllib.request.urlretrieve(url, imageName)
    #image=urllib.URLopener()
    #image.retrieve(url,imageName)  # download comicName at URL

argsDict = {'url' : "variety.com", 'delay': 5, 'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.32 (KHTML, like Gecko) Version/10.0 Mobile/14A5261v Safari/602.1', 'full_page': True}

url = (urlbox(argsDict))
urllib.request.urlretrieve(url, "cat.png")

''' TODO
Create class for JSONIFY arguments
Pass arguments into URL box
Pass new URL into Download image class
'''