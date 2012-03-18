#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import cgi
import yaml
from datetime import datetime
import dbfuncs
import cardtype

from google.appengine.api import users
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

webapp.template.register_template_library('jstfilter')

class MtGCard(db.Model):
    name = db.StringProperty(required=True)
    name_ja = db.StringProperty()
    cost = db.StringProperty()
    MainType = db.IntegerProperty()
    SubType = db.ListProperty(str)

class upload_decklist(webapp.RequestHandler):
    def get(self):
        template_values = {'action':'/upload_decklist'}
        path = os.path.join(os.path.dirname(__file__), 'htdocs/index.html')
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
        deck = cardtype.MtGDeck()
        path = os.path.join(os.path.dirname(__file__), 'htdocs/result.html')
        self.request.charset = 'utf-8'
        upload_file = self.request.get('fileName').decode('utf-8')
        if upload_file:
            now = datetime.now()
            deck.fromString(upload_file)

            num_lands = sum([l[1] for l in deck.MainDeck['Land']])
            num_creatures = sum([l[1] for l in deck.MainDeck['Creature']])
            num_spells = sum([l[1] for l in deck.MainDeck['Spells']])
            num_sideboard = sum(l[1] for l in deck.SideBoard)

            template_values = {'Lands' : deck.MainDeck['Land'],
                               'num_lands' : num_lands,
                               'Creatures' : deck.MainDeck['Creature'],
                               'num_creatures' : num_creatures,
                               'Spells' : deck.MainDeck['Spells'],
                               'num_spells' : num_spells,
                               'num_sideboard' : num_sideboard,
                               'sideboard' : deck.SideBoard}

            self.response.out.write(template.render(path, template_values))

        else:
            template_values = {'action':'/upload_decklist'}
            path = os.path.join(os.path.dirname(__file__), 'htdocs/index.html')
            self.response.out.write(template.render(path, template_values))

class Whatis(webapp.RequestHandler):
    def get(self):
        template_value = {}
        path = os.path.join(os.path.dirname(__file__), 'htdocs/whatsthis.html')
        self.response.out.write(template.render(path, template_value))

class ChangeLog(webapp.RequestHandler):
    def get(self):
        log = dbfuncs.ChangeLogModel.all()
        log.order('-date')
        template_value = {'changelog' : log}
        path = os.path.join(os.path.dirname(__file__), 'htdocs/changelog.html')
        self.response.out.write(template.render(path, template_value))
                                                
application = webapp.WSGIApplication(
    [('/',upload_decklist),
     ('/upload_decklist',upload_decklist),
     ('/whatsthis',Whatis),
     ('/changelog',ChangeLog)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
