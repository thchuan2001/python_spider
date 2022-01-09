# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import csv
from operator import itemgetter

from scrapy import item

class Test1Pipeline:
    def open_spider(self,spider):
        self.result=[]
    def process_item(self, item, spider):
        dict_item = dict(item)
        self.result.append(dict_item)
        return item
    def close_spider(self,spider):  
        with open("./date.txt","r") as f:  
            date="2021-12-"+f.read()
        with open("{}.csv".format(date),"w",newline='',encoding="utf_8_sig") as csvfile:
            writer=csv.writer(csvfile)
            head=["country","total_cases"]
            writer.writerow(head)
            for course in self.result:
                writer.writerow(itemgetter(*head)(course))

