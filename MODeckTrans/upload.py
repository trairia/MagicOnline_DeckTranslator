#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import cgi
import yaml

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
        path = os.path.join(os.path.dirname(__file__), 'upload.html')
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
        upload_file = self.request.get('fileName').split('Sideboard')
        main_deck = upload_file[0].split('\r\n')
        sideboard = None
        if len(upload_file) == 2:
            sideboard = upload_file[1].split('\r\n')

        MainDeck = {}
        for line in main_deck:
            if line == '':
                continue
            tmp = line.split(' ')
            num = int(tmp[0])
            name = ' '.join(tmp[1:])
            MainDeck[name] = MainDeck.get(name, 0) + num

        SideBoard = {}
        if not sideboard:
            return
        
        for line in sideboard:
            if line == '':
                continue
            tmp = line.split(' ')
            num = int(tmp[0])
            name = ' '.join(tmp[1:])
            SideBoard[name] = SideBoard.get(name, 0) + num

        for k,v in MainDeck.items():
            print v,' ',Translate(k)
        print u"\n//side board"
        for k,v in SideBoard.items():
            print v,' ',Translate(k)


class upload_cardlist(webapp.RequestHandler):
    def get(self):
        template_values = {'action':'/upload_cardlist'}
        path = os.path.join(os.path.dirname(__file__), 'upload.html')
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
    [('/',MainPage),
     ('/upload_decklist',upload_decklist),
     ('/upload_cardlist',upload_cardlist)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
