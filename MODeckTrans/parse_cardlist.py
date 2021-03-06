#!/usr/bin/python
# -*- coding:utf-8 -*-
import BeautifulSoup as BS
import codecs

card_type_list ={'Legendary'   :0x8000,
                 'Tribal'      :0x4000,
                 'Land'        :0x0800,
                 'Creature'    :0x0400,
                 'Enchantment' :0x0200,
                 'Artifact'    :0x0100,
                 'Instant'     :0x0080,
                 'Sorcery'     :0x0040,
                 'Planeswalker':0x0020}

def card_type(typestring):
    """
    カードタイプの解析用関数
    """
    delimiter = u'—'
    types = [t for t in typestring.split(delimiter)]
    ret = {'mainType':0,
           'subType':None}

    subType = None
    mainType = types[0].strip().split()

    if len(types) == 2:
        subType = types[1].strip().split()

    for t in mainType:
        ret['mainType'] += card_type_list[t]

    ret['subType'] = subType

    return ret

def load_html(htmlfile):
    fileHandle = None
    try:
        fileHandle = open(htmlfile,'r')
    except IOError:
        print "cannot open file : %s" % htmlfile
    else:
        soup = BS.BeautifulSoup(fileHandle.read().decode('utf-8'))
        tr_tags = soup.findAll(u'tr')
        card_list = []
        card_data = {}
        for node in tr_tags:
            td_tags = node.findAll(u'td')
            if len(td_tags) == 2:
                """
                カードデータの読み込み
                カード[プロパティ:]=値
                の形式で辞書で保存
                """
                a_tag = td_tags[1].find('a')
                txt = None
                prop = td_tags[0].contents[0].strip()[0:-1]
                if not a_tag == None:
                    """
                    カードのプロパティ(Name)
                    """
                    txt = a_tag.contents[0]
                    ja,en = [elem[0:-1] for elem in txt.split('(')]
                    card_data[prop] = {u'ja':ja,u'en':en}
                else:
                    """
                    その他のプロパティはもう一段階深いタグ
                    にあるので、それを取得
                    """
                    txt = td_tags[1].contents[0].strip()
                    card_data[prop] = txt
            
            if len(td_tags) == 1:
                """
                カード1枚の読み込み完了
                次のカードデータを作成
                """
                card_list.append(card_data)
                card_data = {}

        return card_list

def output_list(ofilename, clist):
    try:
        fileHandle = codecs.open(ofilename, 'w','utf_8')
    except IOError:
        print 'cannot open file : %s' % ofilename
    else:
        print ', '.join(clist[0].keys())
        for card in clist:
            c_type = card_type(card['Type'])
            subType = 'null'
            if c_type['subType']:
                subType = ", ".join(c_type['subType'])

            fileHandle.write('- Name_en: %s\n' % card['Name']['en'])
            fileHandle.write('  Name_ja: %s\n' % card['Name']['ja'])
            fileHandle.write('  Cost: %s\n' % card['Cost'])
            fileHandle.write('  MainType: %d\n' % c_type['mainType'])
            fileHandle.write('  SubType: [%s]\n' % subType)
            fileHandle.write(u'\n')
            
def main():
    clist = load_html("DKA.htm")
    output_list("result.txt",clist)
if __name__ == "__main__":
    main()
