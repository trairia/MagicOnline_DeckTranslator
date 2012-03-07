#!/usr/bin/env python
# -*- coding:utf-8 -*-

import yaml

data = yaml.load(open('result.txt').read().decode('utf-8'))
for card in data:
    print card
