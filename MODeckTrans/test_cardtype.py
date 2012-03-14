#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
from cardtype import *

class TestCardType(unittest.TestCase):
    def test_typical_type(self):
        card = card_type_list['Creature']
        result = cardtype(card)
        self.assertEqual(result,'Creature')

        card = card_type_list['Enchantment']
        result = cardtype(card)
        self.assertEqual(result,'Enchantment')

        card = card_type_list['Artifact']
        result = cardtype(card)
        self.assertEqual(result,'Artifact')
        
        card = card_type_list['Instant']
        result = cardtype(card)
        self.assertEqual(result,'Instant')

        card = card_type_list['Sorcery']
        result = cardtype(card)
        self.assertEqual(result,'Sorcery')

        card = card_type_list['Sorcery']
        result = cardtype(card)
        self.assertEqual(result,'Sorcery')

        card = card_type_list['Creature']
        result = cardtype(card)
        self.assertEqual(result,'Creature')

    def test_combination_type(self):
        types = ['Legendary','Creature']
        card = 0
        for t in types:
            card = card | card_type_list[t]
        result = cardtype(card)
        self.assertEqual(result, 'Creature')

        types = ['Basic','Land']
        card = 0
        for t in types:
            card = card | card_type_list[t]
        result = cardtype(card)
        self.assertEqual(result, 'Land')

        types = ['Basic','Snow','Land']
        card = 0
        for t in types:
            card = card | card_type_list[t]
        result = cardtype(card)
        self.assertEqual(result, 'Land')

        types = ['Tribal','Instant']
        card = 0
        for t in types:
            card = card | card_type_list[t]
        result = cardtype(card)
        self.assertEqual(result, 'Instant')

        types = ['Artifact','Creature']
        card = 0
        for t in types:
            card = card | card_type_list[t]
        result = cardtype(card)
        self.assertEqual(result, 'Creature')

        types = ['Legendary','Artifact','Creature']
        card = 0
        for t in types:
            card = card | card_type_list[t]
        result = cardtype(card)
        self.assertEqual(result, 'Creature')

if __name__ == '__main__':
    unittest.main()
