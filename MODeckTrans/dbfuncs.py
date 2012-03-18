#!/usr/bin/env python
# -*- coding:utf-8 -*-

from google.appengine.ext import db

class MtGCard(db.Model):
    name = db.StringProperty(required=True)
    name_ja = db.StringProperty()
    cost = db.StringProperty()
    MainType = db.IntegerProperty()
    SubType = db.ListProperty(str)

class ChangeLogModel(db.Model):
    message = db.TextProperty()
    date    = db.DateTimeProperty(auto_now_add=True)

def getCardFromDS(cardname):
    query = db.Query(MtGCard)
    query.filter('name = ', unicode(cardname))
    result = query.get()
    card = {}
    if result:
        card['Name_en']  = cardname
        card['Name_ja']  = result.name_ja
        card['cost']     = result.cost
        card['mainType'] = result.MainType
        card['subType']  = result.SubType
    else:
        card['Name_en']  = unicode(cardname)
        card['Name_ja']  = unicode(cardname)
        card['cost']     = None
        card['mainType'] = 0
        card['subType']  = None

    return card

def new_or_overwrite(card):
    query = db.Query(MtGCard)
    query.filter('name = ', card['Name_en'])
    result = query.get()
    if result:
        result.name_ja  = card['Name_ja']
        result.cost     = card['Cost']
        result.MainType = card['MainType']
        result.SubType  = card['SubType']
        result.put()
    else:
        obj = MtGCard(name = card['Name_en'],
                      name_ja = card['Name_ja'],
                      cost = card['Cost'],
                      MainType = card['MainType'],
                      SubType = card['SubType'])
        obj.put()
