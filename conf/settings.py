#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'eric'

class app_config:
    port = 10000  # 端口
    enable_ssl = False  # 是否启用ssl证书
    host = "https://www.dingguanyong.com"  # 应用程序访问地址
    is_debug = True  # 是否调试版本
    defaultRoute = "/home"


db_config = {
    "host": "dgyecsdbpublic.mysql.rds.aliyuncs.com",
    "port": 3322,
    "user": "user1",
    "password": "Yhumnuy7GG9x#54",
    "db": "h2_db_dev"
}
