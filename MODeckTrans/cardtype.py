#!/usr/bin/env python
# -*- coding:utf-8 -*-

import dbfuncs

card_type_list ={'Legendary'   :0x8000,
                 'Tribal'      :0x4000,
                 'Basic'       :0x2000,
                 'Snow'        :0x1000,
                 'Land'        :0x0800,
                 'Creature'    :0x0400,
                 'Enchantment' :0x0200,
                 'Artifact'    :0x0100,
                 'Instant'     :0x0080,
                 'Sorcery'     :0x0040,
                 'Planeswalker':0x0020}

def cardtype(typenum):
    if typenum & card_type_list['Land']:
        return 'Land'
    elif typenum & card_type_list['Creature']:
        return 'Creature'
    elif typenum & card_type_list['Enchantment']:
        return 'Enchantment'
    elif typenum & card_type_list['Artifact']:
        return 'Artifact'
    elif typenum & card_type_list['Instant']:
        return 'Instant'
    elif typenum & card_type_list['Sorcery']:
        return 'Sorcery'
    elif typenum & card_type_list['Planeswalker']:
        return 'Planeswalker'

class MtGDeck(object):
    def __init__(self):
        self.MainDeck = {'Land':[],
                         'Creature':[],
                         'Spells':[]}
        self.haveSideBoard = False
        self.SideBoard = []

    def fromString(self, deckstring):
        uploaddata = deckstring.split('Sideboard')
        main_deck = uploaddata[0].split('\n')
        sideboard = None
        maincards = {}

        for line in main_deck:
            tmp = line.strip().split(' ')
            if tmp[0].isdigit():
                num = int(tmp[0])
            else:
                continue
            name = ' '.join(tmp[1:])
            maincards[name] = maincards.get(name, 0) + num

        for name,num in maincards.items():
            card = dbfuncs.getCardFromDS(name)

            if '/' in name:
                # for split card
                name.replace('/','+')

            if cardtype(card['mainType']) == 'Land':
                self.MainDeck['Land'].append((card,num))
            elif cardtype(card['mainType']) == 'Creature':
                self.MainDeck['Creature'].append((card,num))
            else:
                self.MainDeck['Spells'].append((card,num))

        if len(uploaddata) == 2:
            self.haveSideBoard = True
            sideboards = {}
            for line in uploaddata[1].split('\n'):
                tmp = line.strip().split(' ')
                if tmp[0].isdigit():
                    num = int(tmp[0])
                else:
                    continue
                name = ' '.join(tmp[1:])
                sideboards[name] = sideboards.get(name,0) + num

            for name,num in sideboards.items():
                if '/' in name:
                    # for split card
                    name.replace('/','+')

                card = dbfuncs.getCardFromDS(name)
                self.SideBoard.append((card, num))
