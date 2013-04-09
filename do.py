# -*- coding: utf-8 -*-
import webapp2
from google.appengine.ext import db
from cgi import escape
import urllib
import urllib2
from google.appengine.ext import db

class Weibo(db.Model):
    token = db.StringProperty()

class SendWeibo(webapp2.RequestHandler):
    def post(self):
        status = escape(self.request.get('status'))
        if status:
            content =status
            self.response.out.write(content)
            q = db.GqlQuery('select * from Weibo')
            weibo = q.get()
            access_token = weibo.token
            values ={'status':content,
                 'access_token':access_token
                 }
            data = urllib.urlencode(values)
#        self.response.out.write(data)
            url = 'https://api.weibo.com/2/statuses/update.json'
            request = urllib2.Request(url,data)
            u = urllib2.urlopen(request)
        else:
            self.response.out.write('空状态')
    def get(self):
        SendWeibo.post(self)

class testToken(webapp2.RequestHandler):
    def get(self):
#        self.response.out.write()
        q = db.GqlQuery('select * from Weibo')
        weibo = q.get()
        token = weibo.token
        self.response.out.write(token)
        
app = webapp2.WSGIApplication([('/do/sendweibo',SendWeibo),
                               ('/do/testtoken',testToken)],debug=True)