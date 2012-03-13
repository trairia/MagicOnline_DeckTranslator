#!/usr/bin/env python
# -*- coding:utf-8 -*-

from google.appengine.ext import db

class MtGCard(db.Model):
    name = db.StringProperty(required=True)
    name_ja = db.StringProperty()
    cost = db.StringProperty()
    MainType = db.IntegerProperty()
    SubType = db.ListProperty(str)

def getCardFromDS(cardname):
    query = db.Query(MtGCard)
    query.filter('name = ', cardname)
    result = query.get()
    card = {}
    if result:
        card['Name_en']  = cardname
        card['Name_ja']  = result.name_ja
        card['cost']     = result.cost
        card['mainType'] = result.MainType
        card['subType']  = result.SubType
    else:
        card['Name_en']  = cardname
        card['Name_ja']  = cardname
        card['cost']     = None
        card['mainType'] = None
        card['subType']  = None

    return card
