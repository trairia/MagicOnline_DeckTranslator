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


class MtGCard(db.Model):
    name = db.StringProperty(required=True)
    name_ja = db.StringProperty()
    cost = db.StringProperty()
    MainType = db.IntegerProperty()
    SubType = db.ListProperty(str)

def Translate(cardname):
    query = db.Query(MtGCard)
    query.filter('name = ', cardname)
    result = query.get()
    if result:
        return result.name_ja.encode('utf-8')
    else:
        return cardname


class MainPage(webapp.RequestHandler):
    def get(self):
        pass

class upload_decklist(webapp.RequestHandler):
    def get(self):
        template_values = {'action':'/upload_decklist'}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
        deck = cardtype.MtGDeck()
        path = os.path.join(os.path.dirname(__file__), 'result.html')
        upload_file = self.request.get('fileName')
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
            path = os.path.join(os.path.dirname(__file__), 'index.html')
            self.response.out.write(template.render(path, template_values))

class upload_cardlist(webapp.RequestHandler):
    def get(self):
        template_values = {'action':'/upload_cardlist'}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        upload_file = self.request.get('fileName')
        try:
            cardlist = yaml.load(upload_file)
            for card in cardlist:
                if card['SubType'][0] == None:
                    card['SubType'][0] = ''
                
                if str(card['Cost']):
                    card['Cost'] = str(card['Cost'])

                obj = MtGCard(name = card['Name_en'],
                              name_ja = card['Name_ja'],
                              cost = card['Cost'],
                              MainType = card['MainType'],
                              SubType = card['SubType'])
                obj.put()
            self.response.out.write("%d card added" % len(cardlist))
            self.response.out.write("<br>")
            
        except yaml.YAMLError, exc:
            if hasattr(exc, 'probem_mark'):
                mark = exc.problem_mark
                print "Error position: (%s:%s)"%(mark.line+1, mark.column+1)
                                                
application = webapp.WSGIApplication(
    [('/',upload_decklist),
     ('/upload_decklist',upload_decklist),
     ('/upload_cardlist',upload_cardlist)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
