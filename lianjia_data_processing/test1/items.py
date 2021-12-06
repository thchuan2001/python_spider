# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Test1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    pos1=scrapy.Field()
    pos2=scrapy.Field()
    pos3=scrapy.Field()
    room_num=scrapy.Field()
    size=scrapy.Field()
    total_price=scrapy.Field()
    avg_price=scrapy.Field()
    pass
