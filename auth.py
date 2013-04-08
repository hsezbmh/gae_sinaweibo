# -*- coding: utf-8 -*-

from weibo import APIClient
import webapp2
import webbrowser
from google.appengine.ext import db
import urllib2

APP_KEY = 'YOUR_APP_KEY'  # app key
APP_SECRET = 'YOUR_APP_SECRET'  # app secret
CALLBACK_URL = 'YOUR_CALLBACK_URL'  # callback url



class Weibo(db.Model):
    token = db.StringProperty()
#    expires_in = db.IntegerProperty()
class Auth(webapp2.RequestHandler):
    def get(self):
        code = self.request.get('code')
#       self.response.out.write("code:"+code)
        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
        r = client.request_access_token(code)
        access_token = r.access_token
#        expires_in = r.expires_in
#       self.response.out.write("access_token:"+access_token)
        weibo = Weibo()
        weibo.token = access_token
#        weibo.expires_in = expires_in
        weibo.put()
        self.response.out.write("success write into datastore")
class AuthPage(webapp2.RequestHandler):
    def get(self):
        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET,
                   redirect_uri=CALLBACK_URL)
        url = client.get_authorize_url()  # redirect the user to `url'
        self.redirect(url)
        
app = webapp2.WSGIApplication([('/auth', Auth),
                               ('/authpage', AuthPage)],
                                      debug=True)
