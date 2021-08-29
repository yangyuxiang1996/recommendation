#!/usr/bin/env python
# coding=utf-8
'''
Author: Yuxiang Yang
Date: 2021-08-14 21:06:36
LastEditors: Yuxiang Yang
LastEditTime: 2021-08-17 02:28:25
FilePath: /recommendation/dao/mongo_db.py
Description: 
'''
import pymongo


class MongoDB(object):
    def __init__(self, db):
        self.mongo_client = self._connect(
            '127.0.0.1', '27017', 'admin', '123456', db)
        self.db_client = self.mongo_client[db]
        self.connection_test = self.db_client['test_collections']

    def _connect(self, host, port, user, pwd, db):
        mongo_info = self._splicing(host, port, user, pwd, db)
        mongo_client = pymongo.MongoClient(mongo_info, authSource="admin", connect=False, connectTimeoutMS=1200)
        return mongo_client

    @staticmethod
    def _splicing(host, port, user, pwd, db):
        client = 'mongodb://%s:%s' % (str(host), str(port)) + '/'  # 默认
        if user != '':
            client = 'mongodb://%s:%s@%s:%s' % (str(user),
                                                str(pwd), str(host), str(port)) + '/'
            if db != '':
                client += db
        print(client)
        return client

    def test_insert(self):
        test_collection = dict()
        test_collection["name"] = "yangyuxiang"
        test_collection["gender"] = "male"
        self.connection_test.insert_one(test_collection)


if __name__ == "__main__":
    mongo = MongoDB(db='recommendation')
    mongo.test_insert()
