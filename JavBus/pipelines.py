# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
from datetime import datetime
import json
import pymongo
import pymysql
from scrapy.conf import settings

from JavBus.items import MainItem, StarItem


class JsonPipeline(object):
    def __init__(self):
        self.main_file = codecs.open('JavBus.json', 'w', encoding='utf-8')
        self.star_file = codecs.open('JavBus_Star.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # 根据Item的类型保存到不同的文件
        if isinstance(item, MainItem):
            self.main_file.write(line)
        elif isinstance(item, StarItem):
            self.star_file.write(line)
        return item

    def spider_closed(self, spider):
        self.main_file.close()
        self.star_file.close()


class MysqlPipeline(object):
    """
    Mysql保存
    """

    def __init__(self):
        self.conn = pymysql.connect(host=settings['MYSQL_HOST'], user=settings['MYSQL_USER'],
                                    password=settings['MYSQL_PASSWORD'], port=settings['MYSQL_PORT'],
                                    db=settings['MYSQL_DB'])
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            post_item = dict(item)  # 把item转化成字典形式
            if isinstance(item, MainItem):
                # 将MainItem拆分放入多个库
                magnets = post_item['magnets']
                for x in magnets:
                    x['movie_code'] = post_item['code']
                    self.insert_data('magnet', x)
                previews = post_item['previews']
                for x in previews:
                    preview = {
                        'movie_code': post_item['code'],
                        'preview': x
                    }
                    self.insert_data('preview', preview)

                stars = post_item['stars']
                for x in stars:
                    x.pop('name')
                    x['star_code'] = x['code']
                    x.pop('code')
                    x['movie_code'] = post_item['code']
                    self.insert_data('movie_star', x)
                tags = post_item['tags']
                for x in tags:
                    x['censored'] = post_item['censored']
                    self.insert_data('tag', x)
                    self.insert_data('movie_tag', {'movie_code': post_item['code'], 'tag_code': x['code']})
                studio = post_item['studio']
                label = post_item['label']
                director = post_item['director']
                series = post_item['series']
                if studio:
                    self.insert_data('studio', studio)
                    self.insert_data('movie_studio', {'movie_code': post_item['code'], 'studio_code': studio['code']})
                    post_item['studio'] = post_item['studio']['name']
                else:
                    post_item['studio'] = ''
                if label:
                    # self.coll_label.insert(label)
                    self.insert_data('label', label)
                    self.insert_data('movie_label', {'movie_code': post_item['code'], 'label_code': studio['code']})
                    post_item['label'] = post_item['label']['name']
                else:
                    post_item['label'] = ''
                if director:
                    self.insert_data('director', director)
                    self.insert_data('movie_director',
                                     {'movie_code': post_item['code'], 'director_code': studio['code']})
                    post_item['director'] = post_item['director']['name']
                else:
                    post_item['director'] = ''
                if series:
                    self.insert_data('series', series)
                    self.insert_data('movie_series', {'movie_code': post_item['code'], 'series_code': studio['code']})
                    post_item['series'] = post_item['series']['name']
                else:
                    post_item['series'] = ''

                post_item.pop('previews')
                post_item.pop('magnets')
                post_item.pop('tags')
                post_item.pop('stars')
                self.insert_data('movie', post_item)
            elif isinstance(item, StarItem):
                self.insert_data('star', post_item)
            self.conn.commit()
        except:
            self.conn.rollback()
        # return item  # 会在控制台输出原item数据，可以选择不写

    def close_spider(self, spider):
        print('Failed')
        self.cursor.close()
        self.conn.close()

    def insert_data(self, table, data):
        """
        通用插入方法
        :param data:数据
        :param table: 表明
        :return:
        """
        data['updatetime'] = datetime.now()
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys,
                                                                                             values=values)
        update = ','.join([" {key} = %s".format(key=key) for key in data])
        sql += update
        print(sql)
        self.cursor.execute(sql, tuple(data.values()) * 2)


class MongoPipeline(object):
    def __init__(self):
        # 链接数据库
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        self.coll_movie = self.db[settings['MONGO_COLL_MOVIE']]  # 获得movie_collection的句柄
        self.coll_star = self.db[settings['MONGO_COLL_STAR']]  # 获得star_collection的句柄
        self.coll_magnet = self.db[settings['MONGO_COLL_MAGNET']]
        self.coll_preview = self.db[settings['MONGO_COLL_PREVIEW']]
        self.coll_movie_star = self.db[settings['MONGO_COLL_MOVIE_STAR']]

        self.coll_studio = self.db[settings['MONGO_COLL_STUDIO']]
        self.coll_label = self.db[settings['MONGO_COLL_LABEL']]
        self.coll_director = self.db[settings['MONGO_COLL_DIRECTOR']]
        self.coll_series = self.db[settings['MONGO_COLL_SERIES']]
        self.coll_movie_studio = self.db[settings['MONGO_COLL_MOVIE_STUDIO']]
        self.coll_movie_label = self.db[settings['MONGO_COLL_MOVIE_LABEL']]
        self.coll_movie_director = self.db[settings['MONGO_COLL_MOVIE_DIRECTOR']]
        self.coll_movie_series = self.db[settings['MONGO_COLL_MOVIE_SERIES']]
        self.coll_tag = self.db[settings['MONGO_COLL_TAG']]
        self.coll_movie_tag = self.db[settings['MONGO_COLL_MOVIE_TAG']]

    def process_item(self, item, spider):
        postItem = dict(item)  # 把item转化成字典形式
        if isinstance(item, MainItem):
            # 将MainItem拆分放入多个库
            magnets = postItem['magnets']
            for x in magnets:
                x['movie_code'] = postItem['code']
                self.coll_magnet.insert(x)

            previews = postItem['previews']
            for x in previews:
                preview = {
                    'movie_code': postItem['code'],
                    'preview': x
                }
                self.coll_preview.insert(preview)

            stars = postItem['stars']
            for x in stars:
                x.pop('name')
                x['star_code'] = x['code']
                x.pop('code')
                x['movie_code'] = postItem['code']
                self.coll_movie_star.insert(x)

            tags = postItem['tags']
            for x in tags:
                x['censored'] = postItem['censored']
                self.coll_tag.insert(x)
                self.coll_movie_tag.insert({'movie_code': postItem['code'], 'tag_code': x['code']})
            studio = postItem['studio']
            label = postItem['label']
            director = postItem['director']
            series = postItem['series']
            if studio:
                self.coll_studio.insert(studio)
                self.coll_movie_studio.insert({'movie_code': postItem['code'], 'studio_code': studio['code']})
                postItem['studio'] = postItem['studio']['name']
            else:
                postItem['studio'] = ''
            if label:
                self.coll_label.insert(label)
                self.coll_movie_label.insert({'movie_code': postItem['code'], 'label_code': studio['code']})
                postItem['label'] = postItem['label']['name']
            else:
                postItem['label'] = ''
            if director:
                self.coll_director.insert(director)
                self.coll_movie_director.insert({'movie_code': postItem['code'], 'director_code': studio['code']})
                postItem['director'] = postItem['director']['name']
            else:
                postItem['director'] = ''
            if series:
                self.coll_series.insert(series)
                self.coll_movie_series.insert({'movie_code': postItem['code'], 'series_code': studio['code']})
                postItem['series'] = postItem['series']['name']
            else:
                postItem['series'] = ''

            postItem.pop('previews')
            postItem.pop('magnets')
            postItem.pop('tags')
            postItem.pop('stars')

            self.coll_movie.insert(postItem)  # 向数据库插入一条记录
        elif isinstance(item, StarItem):
            self.coll_star.insert(postItem)  # 向数据库插入一条记录
        return item  # 会在控制台输出原item数据，可以选择不写
