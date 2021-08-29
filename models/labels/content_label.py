#!/usr/bin/env python
# coding=utf-8
'''
Author: Yuxiang Yang
Date: 2021-08-14 20:35:23
LastEditors: Yuxiang Yang
LastEditTime: 2021-08-17 02:29:38
FilePath: /recommendation/models/labels/content_label.py
Description: 
'''
import re
import sys
sys.path.append('../../')
from datetime import datetime
from models.labels.entity.content import Content
from sqlalchemy import distinct
from dao.mongo_db import MongoDB
from dao.mysql_db import Mysql
from sqlalchemy import create_engine


class ContentLabel(object):
    def __init__(self):
        self.engine = Mysql()
        self.session = self.engine._DBSession()
        self.mongo = MongoDB(db="recommendation")
        self.collection = self.mongo.db_client['content_labels']

    def get_data_from_mysql(self):
        """
        从mysql中获取数据，字段定义在content.py中
        """
        types = self.session.query(distinct(Content.type))  # 查询表中有多少个重复的type
        for i in types:
            print(i[0])
            res = self.session.query(Content).filter(Content.type == i[0])
            if res.count() > 0:  # 记录数大于0
                for x in res.all():
                    create_time = datetime.utcnow()
                    content_collection = dict()
                    content_collection['describe'] = x.content
                    content_collection['news_date'] = x.date
                    content_collection['type'] = x.type
                    content_collection['title'] = x.title
                    content_collection['tag'] = x.tag
                    content_collection['likes'] = 0
                    content_collection['hot_heat'] = 10000
                    content_collection['read'] = 0
                    content_collection['collections'] = 0
                    content_collection['word_nums'] = self.get_word_nums(x.content)
                    content_collection['keywords'] = ""
                    content_collection['create_time'] = create_time
                    # print(content_collection)
                    self.collection.insert(content_collection)

    def get_word_nums(self, sentence):
        ch = re.findall('([\u4e00-\u9f5a])', sentence)
        return len(ch)


if __name__ == '__main__':
    content_label = ContentLabel()
    content_label.get_data_from_mysql()
    # sentence = "我爱中国！！！I Love China！"
    # print(content_label.get_word_nums(sentence))
