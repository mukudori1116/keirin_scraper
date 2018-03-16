# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class KeirinScraperPipeline(object):
    def process_item(self, item, spider):
        item['odds_table'] = item['odds_table'].to_json(orient='values')
        return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if not isinstance(item['odds_table'], str):
            item['odds_table'] = item['odds_table'].to_json(orient='values')
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
