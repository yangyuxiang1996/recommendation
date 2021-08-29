#!/usr/bin/env python
# coding=utf-8
'''
Author: Yuxiang Yang
Date: 2021-08-14 20:42:55
LastEditors: Yuxiang Yang
LastEditTime: 2021-08-17 01:34:59
FilePath: /recommendation/models/labels/entity/content.py
Description: 
'''
from dao.mysql_db import Mysql
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Content(Base):
    __tablename__ = "data"  # 定义表名
    id = Column(Integer(), primary_key=True)
    date = Column(Text())
    title = Column(Text())
    content = Column(Text())
    type = Column(Text())
    tag = Column(Text())

    def __init__(self):
        self.mysql = Mysql()
        self.engine = self.mysql.engine
        Base.metadata.create_all(self.engine)
