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
        try:
            self.file=open("result.json","w",encoding="utf-8")
        except Exception as err:
            print(err)
        self.result=[]
    def process_item(self, item, spider):
        dict_item = dict(item)
        self.result.append(dict_item)
        return item
    def close_spider(self,spider):    
        self.file.write(json.dumps(self.result,ensure_ascii=False))
        self.file.close()
        with open("result.csv","w",newline='',encoding="utf_8_sig") as csvfile:
            writer=csv.writer(csvfile)
            head=["name","teachers","school","stu_num"]
            writer.writerow(["课程名称","授课教师","学校","学生人数"])
            for course in self.result:
                writer.writerow(itemgetter(*head)(course))

