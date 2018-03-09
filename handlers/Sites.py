#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'eric'

import handlers
from handlers import route


# 官网首页
@route(r"/", "index")
class indexHandler(handlers.RootHandler):
    def get(self, *args, **kwargs):
        self.render("index.html", title="hello")
        # self.write("hello")
        # lib.CookieHelper.logon(self)
        # if self.is_mobile:
        #     self.render("officialSite/mobile/index.html")
        # else:
        #     self.render("officialSite/index.html", currentTab="")

