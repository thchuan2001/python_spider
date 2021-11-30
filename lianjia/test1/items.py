# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Test1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    district=scrapy.Field()
    total_price=scrapy.Field()
    unit_price=scrapy.Field()
    square=scrapy.Field()
    pass
