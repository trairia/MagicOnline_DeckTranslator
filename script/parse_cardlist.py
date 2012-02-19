#!/usr/bin/python
# -*- coding:utf-8 -*-
import BeautifulSoup as BS
import codecs
"""
Card Properties
"""

def load_html(htmlfile):
    fileHandle = None
    try:
        fileHandle = open(htmlfile,'r')
    except IOError:
        print "cannot open file : %s" % htmlfile
    else:
        soup = BS.BeautifulSoup(fileHandle.read())
        tr_tags = soup.findAll('tr')
        card_list = []
        card_data = {}
        for node in tr_tags:
            td_tags = node.findAll('td')
            if len(td_tags) == 2:
                a_tag = td_tags[1].find('a')
                txt = None
                if not a_tag == None:
                    txt = a_tag.contents[0]
                else:
                    txt = td_tags[1].contents[0].strip()
                prop = td_tags[0].contents[0].strip()
                card_data[prop] = txt
 
            if len(td_tags) == 1:
                card_list.append(card_data)
                card_data = {}

        return card_list

def output_list(ofilename, clist):
    try:
        fileHandle = codecs.open(ofilename, 'w','utf_8')
    except IOError:
        print 'cannot open file : %s' % ofilename
    else:
        for card in clist:
            for k,v in card.iteritems():
                fileHandle.write(u"%s%s\n"%(k,v))
def main():
    clist = load_html("DKA.htm")
    output_list("result.txt",clist)
if __name__ == "__main__":
    main()
