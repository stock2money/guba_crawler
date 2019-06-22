# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import sys
sys.path.append("./news-emotion")
from demo import Predictor, save_model

class GubaStockReviewsSpiderPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host="127.0.0.1",
            db="mydb",
            user="root",
            passwd="password",
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

        best_vector = "wordfreq"
        best_model = 1  # linearLogistic
        save_model(best_vector, best_model)
        self.predictor = Predictor()
        self.predictor.load_model()
        self.predictor.set_mode(mode="wordfreq")

    def process_item(self, item, spider):
        if item["infoType"] == '1':
            sql = "INSERT INTO comment(title, detail, time, href, code, author, emotion) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            try:
                if item['detail'] == '' or item['detail'] == None:
                    return item
                self.predictor.set_news(news=item["detail"])
                self.predictor.trans_vec()
                tag = str(self.predictor()[0])
                self.cursor.execute(sql, (item['title'], item['detail'], item['time'], item['href'], item['code'], item['author'], tag))
                self.cursor.connection.commit()
            except BaseException as e:
                print(e)
                print("相关评论已经存在")
                self.connect.rollback()
        else:
            sql = "INSERT INTO news(time, title, href, detail) VALUES(%s,%s,%s,%s)"
            try:
                if item['detail'] == '' or item['detail'] == None:
                    return item
                self.cursor.execute(
                    sql, (item['time'], item['title'], item['href'], item['detail']))
                self.cursor.connection.commit()
            except BaseException as e:
                print(e)
                print("文章已存在")
                self.connect.rollback()
        return item
