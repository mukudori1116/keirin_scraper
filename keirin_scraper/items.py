# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KeirinScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    race_id = scrapy.Field()
    player1 = scrapy.Field()
    player2 = scrapy.Field()
    player3 = scrapy.Field()
    player4 = scrapy.Field()
    player5 = scrapy.Field()
    player6 = scrapy.Field()
    player7 = scrapy.Field()
    player8 = scrapy.Field()
    player9 = scrapy.Field()
    odds_table = scrapy.Field()
