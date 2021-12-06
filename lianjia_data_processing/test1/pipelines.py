# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
from operator import itemgetter

class Test1Pipeline:
    def open_spider(self,spider):
        self.result=[]
    def process_item(self, item, spider):
        dict_item = dict(item)
        self.result.append(dict_item)
        return item
    def close_spider(self,spider):
        with open("result.csv","w",newline='',encoding="utf_8_sig") as csvfile:
            writer=csv.writer(csvfile)
            head=["name","pos1","pos2","pos3","room_num","size","total_price","avg_price"]
            writer.writerow(head)
            for house in self.result:
                writer.writerow(itemgetter(*head)(house))
