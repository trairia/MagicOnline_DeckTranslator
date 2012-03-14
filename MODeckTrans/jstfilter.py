#!/usr/bin/env python
# -*- coding:utf-8 -*-

from google.appengine.ext import webapp

import datetime
import dateutil.tz

register = webapp.template.create_template_register()

def jst(value):
    return value.replace(tzinfo=dateutil.tz.tzutc()).astimezone(dateutil.tz.gettz('Asia/Tokyo'))

register.filter(jst)
