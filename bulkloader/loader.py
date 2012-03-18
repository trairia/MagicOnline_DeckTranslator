#!usr/bin/env python

from google.appengine.tools import bulkloader
from dbfuncs import MtGCard
import yaml
import codecs

class DataLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'MtGCard',
                                   [('name', unicode),
                                    ('name_ja', unicode),
                                    ('cost',str),
                                    ('MainType',int),
                                    ('SubType',list)])

    def generate_key(self, i, values):
        return values[0]

    def generate_records(self, filename):
        fileHandle = codecs.open(filename, 'r', encoding='utf-8')
        def generator():
            for card in yaml.load(fileHandle.read()):
                subtype = [] if card['SubType'][0]==None else card['SubType']
                yield [card['Name_en'],
                       card['Name_ja'],
                       card['Cost'],
                       card['MainType'],
                       subtype
                    ]
            
        return generator()

loaders = [DataLoader]
