#!/usr/bin/env python
# coding=utf-8
'''
Author: Yuxiang Yang
Date: 2021-08-14 20:28:49
LastEditors: Yuxiang Yang
LastEditTime: 2021-08-17 01:33:03
FilePath: /recommendation/dao/mysql_db.py
Description: 
'''
import sys
sys.path.append('..')
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker


class Mysql(object):
    def __init__(self):
        Base = declarative_base()  # 使用Declarative的方法就是创建一个基类，之后创建的所有映射数据表的类都继承自该基类，该基类用于维护所有映射类的元信息
        self.engine = create_engine(
            'mysql+pymysql://root:123456@localhost:3306/sina', encoding='utf-8')  # 使用create_engine来创建Engine对象
        # Base.metadata.create_all(self.engine)  # 根据映射类创建表
        self._DBSession = sessionmaker(bind=self.engine)  # 使用session可以实现对数据库的增、删、改、查