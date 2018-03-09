#!/usr/bin/python
# -*-coding:utf-8-*-
__author__ = 'Kim'

import json
from operator import itemgetter, attrgetter
import copy
import types


class _:
    """
    python Linq
    """

    def __init__(self, datas):
        self.data = datas
        self.__count()

    def __getData(self):
        """
        获取可用数据
        :return:list
        """
        if not hasattr(self, "result"):
            temp = self.data
        else:
            temp = self.result

        return temp

    def select(self, keys_func=lambda x: x):
        """
        获取所需的属性
        :param keys_func: 关键字表达式
        :return:list
        """
        self.result = [keys_func(x) for x in self.__getData()]
        return self

    def where(self, func):
        """
        根据条件查询
        :param func:lambda表达式
        :return: Linq object
        """

        self.result = [x for x in self.__getData() if func(x)]
        self.__count()
        return self

    def distinct_json(self, key):
        _t_set = {}
        for d in self.__getData():
            if _t_set.has_key(d[key]):
                continue
            _t_set[d[key]] = d
        _tl = []
        for d in _t_set:
            _tl.append(_t_set[d])
        self.result = _tl
        self.__count()
        return self

    # def list2dict(self, key):
    #     result = {}
    #     for r in self.__getData():
    #         result[r[key]] = r[key]
    #         del result[r[key]][key]
    #     return result

    def __dict2list(self, jsonObj, key_name, item_name):
        """
        将dict转换为list，目前供group_by使用，酌情支持其它函数使用
        :param jsonObj:json object
        :param key_name:key的名称
        :param item_name:item的名称
        :return:list
        """
        listObj = []
        for obj in jsonObj:
            listObj.append({key_name: json.loads(obj), item_name: jsonObj[obj]})
        return listObj

    def group_by(self, key_func=lambda x: x, value_func=lambda x: x, key_name="key", item_name="items",
                 item_orderby_key=None, item_orderby_asc=True, key_orderby_key=None, key_orderby_asc=True):
        """
        分组
        :param key_func:key的lambda表达式
        :param value_func: value的lambda表达式
        :param key_name:key的名称
        :param item_name:item的名称
        :return:Python object
        """
        tj = {}
        for d in self.__getData():
            key = key_func(d)
            key = json.dumps(key)
            value = value_func(d)
            if not tj.has_key(key):
                tj[key] = []
            tj[key].append(value)
        self.result = self.__dict2list(tj, key_name, item_name)
        if item_orderby_key is not None:
            for r in self.result:
                r[item_name] = self.__order_by(r[item_name], item_orderby_key, item_orderby_asc)
        if key_orderby_key:
            def key_sort(r):
                return r[key_name][key_orderby_key]

            self.result = self.__order_by(self.result, key_sort, key_orderby_asc)
        self.__count()
        return self

    def __order_by(self, source, key, asc=True):
        if hasattr(key, '__call__'):
            return sorted(source, key=key, reverse=not asc)
        k_t = key if isinstance(key, tuple) else (key,)
        return sorted(source, key=itemgetter(*k_t), reverse=not asc)

    def order_by(self, key, asc=True):
        """
        排序
        :param key:排序关键字，如有多个则传递元组
        :param asc: 是否增序，True为增序，False为倒序，默认为增序
        :return:list
        """

        self.result = self.__order_by(self.__getData(), key, asc)
        return self

    def to_list(self):
        """
        将查询结果转换为list
        :return: list
        """
        return copy.deepcopy(self.result)

    def __count(self):
        """
        统计Linq 结果的总数
        :return:
        """
        self.count = len(self.__getData())

    def first(self, func):
        """
        获取出第一个符合条件的数据
        :param func:
        :return:
        """
        r = [x for x in self.__getData() if func(x)]
        return None if len(r) == 0 else r[0]

    def merge(self, _list, key, isAll=False):
        """
        合并list
        :param _list:将要合并的list
        :param key: 依据key，(src_key,tar_key),key，[src_key,tar_key]
        :param isAll:是否将_list中key不匹配的数据追加进来
        :return:list
        """
        if isinstance(key, basestring):
            source_key, target_key = key, key
        elif isinstance(key, tuple):
            source_key, target_key = key
        else:
            source_key = key["src_key"]
            target_key = key["target_key"]
        rlist = []
        for l in self.__getData():
            first = _(_list).first(lambda x: x[target_key] == l[source_key])
            rlist.append(l)
            if first is not None:
                rlist[len(rlist) - 1].update(first)
                if source_key != target_key:
                    del rlist[len(rlist) - 1][target_key]
        if isAll:
            for l in _list:
                first = _(rlist).first(lambda x: x[source_key] == l[target_key])
                if first is None:
                    rlist.append(l)
                    if source_key != target_key:
                        rlist[len(rlist) - 1][source_key] = rlist[len(rlist) - 1][target_key]
                        del rlist[len(rlist) - 1][target_key]

        self.result = rlist
        return self

    def distinct(self, func):
        """
        获取唯一值列表
        :param func: 函数或key
        :return:
        """
        r = [func(x) if isinstance(func, types.FunctionType) else x[func] for x in self.__getData()]
        r = list(set(r))
        return copy.deepcopy(r)

    def sum(self, key_func):
        """
        求和，求得指定属性的和
        :param key_func: 函数或key
        :return:
        """
        r = [key_func(x) if isinstance(key_func, types.FunctionType) else x[key_func] for x in self.__getData()]
        return sum(r)

    def pluck(self, key):
        """
        萃取数组对象中某属性值，返回一个数组
        :param key:属性名称
        :return:
        """
        return [x[key] for x in self.__getData()]

# if __name__ == "__main__":
#     arr = [
#         {"id": 1, "name": "张三"},
#         {"id": 2, "name": "李四"},
#         {"id": 3, "name": "王五"},
#         {"id": 4, "name": "赵六"},
#         {"id": 5, "name": "卓七"},
#     ]
#     _l = [
#         {"iid": 1, "sex": "男"},
#         {"iid": 3, "sex": "女"},
#         {"iid": 5, "sex": "男"},
#         {"iid": 7, "sex": "女"},
#         {"iid": 9, "sex": "女"},
#     ]
#     print(arr + _l)
#     en = _(arr).merge(_l, ("id", "iid"), True).to_list()
#     print(en)
