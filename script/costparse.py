#!/usr/bin/env python

generic, hybrid, basic = xrange(3)

class costelem(object):
    def __init__(self, t = None, c = None, s = 0):
        self.costtype = t
        self.cost     = c
        self.size     = s


class CostParser(object):
    def __init__(self):
        self.mode = CostParser.generic
        

    def parse(self, string):
        ret = []
        for c in string:
            print c

