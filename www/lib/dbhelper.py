# -*-coding:utf-8-*-
__author__ = 'eric'
# import threading, time, datetime
from db import Mysql


class dbhelper(Mysql):
    def innertTable(self, table_name, data):
        sql = self.insertSql(table_name=table_name, data=data)
        return self.insertOne(sql, value=None)

    def updateTable(self, table_name=None, data=None, where=None):
        sql = self.updateSql(data=data, table_name=table_name, where=where)
        print sql
        ret = self.update(sql, param=None)
        return ret

    def selectAll(self,table_name=None, where=None,select=None):
        sql = self.selectsql(table_name=table_name,where=where,select="*")
        data = self.getAll(sql)
        return data

    def selectOne(self, table_name=None, data=None, where=None):
        sql = self.selectsql(table_name=table_name, where=where, select="*")
        data = self.getOne(sql)
        return data

    def deletesql(self,table_name=None, data=None, where=None):
        sql = self.deletesql(table_name=table_name, where=where)
        data = self.delete(sql)
        return data

    def insertSql(self, table_name, data):
        sql = "insert into `%(table)s` (%(keys)s) VALUES (%(values)s)"
        if isinstance(data, (tuple, list, set)):
            keys = ["`%s`" % x[1] for x in data]
        else:
            keys = ["`%s`" % x for x in data.keys()]

        if isinstance(data, (tuple, list, set)):
            values = ["'%s'" % key[1] for key in data]
        else:
            values = ["'%s'" % data[key] for key in data.keys()]

        param = {
            "table": table_name,
            "keys": ",".join(keys),
            "values": ",".join(values)
        }
        return sql % param

    def updateSql(self, table_name, data, where):
        sql = "update `%(table)s` set  %(keys)s  where %(where)s"
        if isinstance(data, (tuple, list, set)):
            updateFiled = ["`%s` = '%s'" % (x, y) for x, y in data]
        else:
            updateFiled = ["`%s` = '%s'" % (x, data[x]) for x in data.keys()]

        if isinstance(where, (tuple, list, set)):
            where = ["`%s` = '%s'" % (x, y) for x, y in where]
        else:
            where = ["`%s` = '%s'" % (x, where[x]) for x in where.keys()]
        param = {
            "table": table_name,
            "keys": ",".join(updateFiled),
            "where": " and ".join(where)
        }
        sql = sql % param
        return sql

    def selectsql(self, table_name, where, select="*"):
        sql = "select %(select)s from %(table)s where %(where)s"
        if isinstance(where, (tuple, list, set)):
            where = ["`%(key)s`= '%(value)s' " % (key[0], key[1]) for key in where]
        else:
            where = ["`%(key)s`= '%(value)s' " % (key, where[key]) for key in where]
        param = {
            "table": table_name,
            "select": select,
            "where": " and ".join(where)
        }
        sql = sql % param
        return sql

    def deletesql(self, table_name, where):
        sql = "delete from %(table)s where %(where)s"
        if isinstance(where, (tuple, list, set)):
            where = ["`%(key)s`= '%(value)s' " % (key[0], key[1]) for key in where]
        else:
            where = ["`%(key)s`= '%(value)s' " % (key, where[key]) for key in where]
        param = {
            "table": table_name,
            "where": " and ".join(where)
        }
        sql = sql % param
        return sql

# dbhelper = dbhelper()
# print dbhelper.updateTable("pec_account_record", data={"identity_id": "10", "order_id": "10"}, where=[["id", 4]])
# dbhelper.commit()
