# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
from scrapy.conf import settings


class AppPipeline(object):
    def open_spider(self, spider):
        path = settings.get('TMP_FOLDER')
        if not os.path.exists(path):
            os.makedirs(path)
        self.file = open(f'{path}/{spider.name}.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
