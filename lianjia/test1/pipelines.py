# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class Test1Pipeline:
    def open_spider(self,spider):
        try:
            self.file=open("result.json","w",encoding="utf-8")
        except Exception as err:
            print(err)
        self.json_str=[]
    def process_item(self, item, spider):
        dict_item = dict(item)
        self.json_str.append(dict_item)
        return item
    def close_spider(self,spider):
        self.file.write(json.dumps(self.json_str,ensure_ascii=False))
        self.file.close()
