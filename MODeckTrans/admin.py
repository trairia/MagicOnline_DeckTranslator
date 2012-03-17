#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import cgi
import yaml
import dbfuncs
import cardtype

from google.appengine.api import users
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

    

class upload_cardlist(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'htdocs/admin.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        upload_file = self.request.get('fileName')
        path = os.path.join(os.path.dirname(__file__), 'htdocs/admin.html')
        message = self.request.get('message')
        if upload_file:
            cardlist = yaml.load(upload_file)
            for card in cardlist:
                if card['SubType'][0] == None:
                    card['SubType'][0] = ''
                
                if str(card['Cost']):
                    card['Cost'] = str(card['Cost'])

                dbfuncs.new_or_overwrite(card)
            
            result = len(cardlist)
            template_values = {'result' : result}
            self.response.out.write(template.render(path, template_values))

        if message:
            template_values = {'result' : None}
            changelog = dbfuncs.ChangeLogModel()
            changelog.message = message
            changelog.put()
            self.response.out.write(template.render(path,template_values))

application = webapp.WSGIApplication(
    [('/admin',upload_cardlist)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
