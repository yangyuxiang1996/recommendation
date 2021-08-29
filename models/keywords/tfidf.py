#!/usr/bin/env python
# coding=utf-8
'''
Author: Yuxiang Yang
Date: 2021-08-17 02:34:28
LastEditors: Yuxiang Yang
LastEditTime: 2021-08-18 17:53:08
FilePath: /recommendation/models/keywords/tfidf.py
Description: 
'''
import jieba
import numpy as np
import heapq
import time
import re
from collections import Counter
from jieba import analyse


class keywordExtractor():
    def __init__(self):
        idf_dict = {}
        data_list = []
        with open("./idf.txt") as f:
            for line in f:
                ll = line.strip().split(" ")
                if len(ll) != 2:
                    continue
                if ll[0] not in idf_dict:
                    idf_dict[ll[0]] = float(ll[1])
                data_list.append(float(ll[1]))
        self.__idf_dict = idf_dict
        self.median = np.median(data_list)
        self.stop_words = self.load_stop_words("./stop_words.txt")

    def load_stop_words(self, path):
        print("加载停用词")
        stop_words = set()
        with open(path, "r") as f:
            for line in f.readlines():
                line = line.strip()
                stop_words.add(line)
        return stop_words
        
    def get_idf(self,word):
        return self.__idf_dict.get(word, self.median)

    def clean_data(self, sent, sep='<'):
        '''
        @description: 过滤无用符号，假如前后空格，避免影响分词结果
        @param {type}
        sent: 句子
        sep: 分隔符是以< or [ 开头
        @return: string 清洗后的句子
        '''
        sent = re.sub(
            r"[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）：]+", "", sent)
        return sent
    
    def predict(self, query, top_n = 1, withWeight=True):
        if len(query) <= 2:
            return [query]
    
        # 切词
        query = self.clean_data(query)
        word_list = list(jieba.cut(query))

        # 去除停用词
        word_list = [word for word in word_list if word not in self.stop_words and len(word) >= 2]
        # print(word_list)
        tf = Counter(word_list)
        n = sum(tf.values())
        
        if len(word_list) < top_n:
            return word_list
        
        # 默认赋值
        idf_list = []
        word_list = list(set(word_list))
        for word in word_list:
            idf_list.append(self.get_idf(word)*tf[word]/n)
        
        # 归一化
        zip_list = zip(range(len(idf_list)), idf_list)
        n_large_idx = [i[0] for i in heapq.nlargest(top_n, zip_list, key=lambda x:x[1])]

        if withWeight:
            return [(word_list[i], idf_list[i]) for i in n_large_idx]
        else:
            return [word_list[i] for i in n_large_idx]
    
if __name__ == "__main__":
    keyword_extractor = keywordExtractor()
    query = "原标题：香港新增2例输入新冠肺炎确诊病例香港特区政府卫生署卫生防护中心8月14日公布，截至当日零时，香港新增2例新冠肺炎确诊病例，均为输入病例。目前，香港累计报告新冠肺炎确诊病例12032例。（总台记者）"
    query = "淡黄的长裙，蓬松的头发 牵着我的手看最新展出的油画"
    start = time.time()
    print(keyword_extractor.predict(query, 5))
    print("提取关键词用时：%s" % (time.time() - start) + "s")
    start = time.time()
    print(analyse.extract_tags(query, 5, withWeight=True))
    print("提取关键词用时：%s" % (time.time() - start) + "s")
    