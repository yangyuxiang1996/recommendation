#!/usr/bin/env python
# coding=utf-8
'''
Author: Yuxiang Yang
Date: 2021-08-19 17:28:29
LastEditors: Yuxiang Yang
LastEditTime: 2021-08-19 22:15:35
FilePath: /recommendation/models/keywords/textrank.py
Description: 
'''
import jieba.posseg
import jieba.analyse
import numpy as np
import heapq


class TextRank(object):
    def __init__(self):
        self.d = 0.85
        self.stop_words = self.load_stop_words("./stop_words.txt")
        self.iter = 10
        self.word2id = {}
        self.id2word = {}
        self.tokenizer = jieba.posseg.dt
        self.allowPOS = ['ns', 'n', 'vn', 'v']
        self.window_size = 5
        self.graph = []
        self.eps = 1e-6

    def load_stop_words(self, path):
        print("加载停用词")
        stop_words = set()
        with open(path, "r") as f:
            for line in f.readlines():
                line = line.strip()
                stop_words.add(line)
        return stop_words

    def tokenize(self, sentence):
        return self.tokenizer.cut(sentence)

    def pair_filter(self, wp):
        return wp.flag in self.allowPOS \
                and len(wp.word.strip()) >= 2 \
                and wp.word not in self.stop_words

    def extract_tags(self, sentence, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'), withFlag=False):
        if allowPOS is not None:
            self.allowPOS = allowPOS
        
        sentence = list(self.tokenize(sentence))
        clean_sent = [wp for wp in sentence if self.pair_filter(wp)]
        for wp in clean_sent:
            if wp.word not in self.word2id:
                self.word2id[wp.word] = len(self.word2id)
    
        self.id2word = {i: word for word, i in self.word2id.items()}
        self.graph = np.zeros(shape=(len(self.word2id), len(self.word2id)))
        self.ws = np.ones(len(self.word2id)) / len(self.word2id)

        for i, wp in enumerate(sentence):
            if wp.word in self.word2id:
                a = self.word2id[wp.word]
                for j in range(i+1, i+self.window_size):
                    if j >= len(sentence):
                        break
                    if sentence[j].word in self.word2id:
                        b = self.word2id[sentence[j].word]
                        self.graph[a][b] += 1
                        self.graph[b][a] += 1
        
        self.graph = self.graph / (np.sum(self.graph, axis=0) + self.eps)
        for i in range(self.iter):
            self.ws = (1 - self.d) + self.d * np.dot(self.graph, self.ws)  
            
        max_ws, min_ws = np.max(self.ws), np.min(self.ws)
        self.ws = (self.ws - min_ws / 10.0) / (max_ws - min_ws / 10.0)

        # 取topK
        zip_list = zip(range(len(self.ws)), self.ws)
        n_large_idx = [i[0] for i in heapq.nlargest(topK, zip_list, key=lambda x:x[1])]

        if withWeight:
            return [(self.id2word[i], self.ws[i]) for i in n_large_idx]
        else:
            return [self.id2word[i] for i in n_large_idx]


if __name__ == '__main__':
    query = "原标题：香港新增2例输入新冠肺炎确诊病例香港特区政府卫生署卫生防护中心8月14日公布，截至当日零时，香港新增2例新冠肺炎确诊病例，均为输入病例。目前，香港累计报告新冠肺炎确诊病例12032例。（总台记者）"
    tr = jieba.analyse.TextRank()
    print(tr.extract_tags(sentence=query, topK=5, withWeight=True))
    tr = TextRank()
    print(tr.extract_tags(sentence=query, topK=5, withWeight=True))

    




                

        
