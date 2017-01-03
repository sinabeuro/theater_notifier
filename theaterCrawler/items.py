# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TheatercrawlerItem(scrapy.Item):
    theatercode = scrapy.Field()
    areacode = scrapy.Field()
    date = scrapy.Field()
    moviename = scrapy.Field()