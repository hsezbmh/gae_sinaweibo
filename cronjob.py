# -*- coding: utf-8 -*-
import sys
import time
import urllib
import urllib2
reload(sys)
sys.setdefaultencoding('utf-8')
import webapp2
from google.appengine.ext import db
import datetime
from cgi import escape

class Task(db.Model):
    datetime = db.DateTimeProperty()
    type = db.StringProperty()
    content = db.StringProperty()
    finished = db.BooleanProperty()
    
class AddTask(webapp2.RequestHandler):
    def post(self):
        task = Task()
        strdate = self.request.get("date")
        strtime = escape(self.request.get("time"))
        stringDateTime = strdate + " " + strtime
        finaldate = datetime.datetime.fromtimestamp(time.mktime(time.strptime(stringDateTime, "%Y-%m-%d %H:%M")))
        task.datetime = finaldate
        task.type = "sina"
        task.content = escape(self.request.get("status"))
        task.finished = False
        task.put()
        
class AutoSend(webapp2.RequestHandler):
    def ontime(self, task):
        serverdatetime = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        if serverdatetime.date() == task.datetime.date():
            if serverdatetime.time().hour == task.datetime.time().hour:
                if abs(serverdatetime.time().minute - task.datetime.time().minute) <= 1:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    def get(self):
        q = db.GqlQuery("select * from Task where finished = False")
        if q:
            for task in q:
                if self.ontime(task):
                    content = task.content
                    values = {'status':content
                              }
                    data = urllib.urlencode(values)
                    url = 'https://xxx.appspot.com/do/sendweibo'
                    request = urllib2.Request(url, data)
                    urllib2.urlopen(request)
                    task.finished = True
                    task.put()



app = webapp2.WSGIApplication([('/cron/autosend', AutoSend),
                               ('/cron/addtask', AddTask)], debug=True)
