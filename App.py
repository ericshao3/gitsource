#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Kim'

import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import socket
import os
import sys
import logging
from lib.LogHelper import LogInit
import conf.settings
LogInit('loggingApp.conf')
from handlers import Route
# from Config.settings import app_config
# from handler import Sites, Catalog, Classes, Class_design, Target, Notice, Dispatch_class, Buyer, Order, Checklist, Job, Users, Feedback, Knowledge, Test, Organization, Report, Offcial
from handlers import RootHandler,Sites
from conf.settings import app_config
# from handler import Offcial, Sites, H5, Common, Buyer, Manage_Set, Target, Knowledge, Notice, Users, Classes, \
# 	Test, Order, Checklist, Class_design, AppReport, Medal, Buyer_product, CheckInNode, Home, Device, pvu_analysis, \
# 	CommonConfig, OffClass__Test, plateform_feedback, buyer_category_list, product_list, Project, category, node_job
# from handler.pec import numbers, teacher, exam_notice, question_feedback, student, pec_number, news_flash, webreport
# ##OffTest, OffClass
# from handler.WebReport import Common, Checklist, Class, Test, Target, Feedback, CheckIn, Project, Product, Bb, kb, \
# 	Improve, report, store_visitor, personal_sale, medal
# import handler.WebReport
# # from handler.admin import Class_design, Discount_design, Admin_Test, Admin_Checklist, config_design, MrDing, LabMate, \
# #     Sites, Authority
# # from handler import h5
# from handler import admin3
# # from handler.DemoProject import Wechat, Form, Sites
# # from handler import Wechat
# from handler import DevelopHelp
# from handler.Tests import img_upload, cookie_test, sync_async
#
# from handler.tasks import task

class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            "upload_path": os.path.join(os.path.dirname(__file__), 'upload'),
            "temp_path": os.path.join(os.path.dirname(__file__), '_temp'),
            "download_path": os.path.join(os.path.dirname(__file__), 'download'),
            "template_path": os.path.join(os.path.dirname(__file__), "templates"),
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "static_temp_path": os.path.join(os.path.dirname(__file__), 'static', '_temp'),
            "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            "login_url": "/login",
            "xsrf_cookies": False,
            "debug": True
        }
        routes = []
        routes += Route.routes()
        routes.append((r".*", RootHandler))
        tornado.web.Application.__init__(self, routes, **settings)


if __name__ == '__main__':

    port = None
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port =  app_config.port
    app = Application()
    listen_attrs = {"xheaders": True}
    http_server = tornado.httpserver.HTTPServer(app, **listen_attrs)

    http_server.listen(port)
    logging.debug(
        "start run Web module. please access http://%s:%s" % (socket.gethostbyname(socket.gethostname()), port))
    loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(loop)
    loop.start()
