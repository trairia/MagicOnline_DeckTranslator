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

        path = os.path.join(os.path.dirname(__file__), 'htdocs/result.html')
        self.request.charset = 'utf-8'
        upload_file = self.request.get('fileName').decode('utf-8')
        textdeck = self.request.get('textdeck')#.decode('utf-8')

        if upload_file:
            self.renderDeck(upload_file)

        elif textdeck:
            self.renderDeck(textdeck)

        else:
            template_values = {'action':'/upload_decklist'}
            path = os.path.join(os.path.dirname(__file__), 'htdocs/index.html')
            self.response.out.write(template.render(path, template_values))

    def renderDeck(self, deck):
        deckdata = cardtype.MtGDeck()
        path = os.path.join(os.path.dirname(__file__), 'htdocs/result.html')
        deckdata.fromString(deck)
        num_lands = sum([l[1] for l in deckdata.MainDeck['Land']])
        num_creatures = sum([l[1] for l in deckdata.MainDeck['Creature']])
        num_spells = sum([l[1] for l in deckdata.MainDeck['Spells']])

        if not (len(deckdata.SideBoard)):
            num_sideboard = 0
        else:
            num_sideboard = sum(l[1] for l in deckdata.SideBoard)

        template_values = {'Lands' : deckdata.MainDeck['Land'],
                           'num_lands' : num_lands,
                           'Creatures' : deckdata.MainDeck['Creature'],
                           'num_creatures' : num_creatures,
                           'Spells' : deckdata.MainDeck['Spells'],
                           'num_spells' : num_spells,
                           'num_sideboard' : num_sideboard,
                           'sideboard' : deckdata.SideBoard}

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
    debug=False)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
