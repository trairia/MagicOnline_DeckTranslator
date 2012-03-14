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
        path = os.path.join(os.path.dirname(__file__), 'admin.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        upload_file = self.request.get('fileName')
        message = self.request.get('message')
        try:
            cardlist = yaml.load(upload_file)
            for card in cardlist:
                if card['SubType'][0] == None:
                    card['SubType'][0] = ''
                
                if str(card['Cost']):
                    card['Cost'] = str(card['Cost'])

                dbfuncs.new_or_overwrite(card)
            self.response.out.write("%d card added" % len(cardlist))
            self.response.out.write("<br>")
            changelog = dbfuncs.ChangeLog()
            changelog.message = message
            changelog.put
            
        except yaml.YAMLError, exc:
            if hasattr(exc, 'probem_mark'):
                mark = exc.problem_mark
                print "Error position: (%s:%s)"%(mark.line+1, mark.column+1)

application = webapp.WSGIApplication(
    [('/admin',upload_cardlist)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
