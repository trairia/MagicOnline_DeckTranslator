#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import cgi

from google.appengine.api import users
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    def get(self):
        pass

class upload(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'upload.html')
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
        upload_file = self.request.get('fileName').split('Sideboard')
        main_deck = upload_file[0].split('\r\n')
        sideboard = None
        if len(upload_file) == 2:
            sideboard = upload_file[1].split('\r\n')
        print main_deck
        print sideboard

        # for line in upload_file:
        #     self.response.out.write(line)
        #     self.response.out.write('<br>')
#        self.response.out.write(upload_file)

application = webapp.WSGIApplication(
    [('/',MainPage),
     ('/upload',upload)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
