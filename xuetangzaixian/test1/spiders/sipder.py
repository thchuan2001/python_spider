import scrapy
from scrapy.http import request, response
from test1.items import Test1Item
import time
class mySpider(scrapy.spiders.Spider):
    name="bupt"
    allowed_domains=["www.xuetangx.com/"]
    start_urls=["https://www.xuetangx.com/search?query=&org=&classify=1&type=&status=&page="]
    def start_requests(self):
        for url in self.start_urls:
            for page_num in range(1,53):
                yield scrapy.Request(url+str(page_num),callback=self.parse,dont_filter=True,cb_kwargs={"url":url+str(page_num)})
    def parse(self,responce,**kwargs):
        self.logger.info(kwargs.get("page_num"))
        item=Test1Item()
        cnt=0
        self.logger.info("==========================================")
        for each in responce.xpath("/html/body/div[1]/div/div[2]/div[1]/div[1]/div[2]/div[1]/*"):
            item.clear()
            item['name']=each.xpath("./div[2]/p[1]/span[1]/text()").get()
            for i in each.xpath("./div[2]/p[2]/*"):
                t=i.xpath("./@class").get()
                self.logger.info(t)
                if (t=="teacher_con"):
                    teacher=""
                    for a in i.xpath("./*"):
                        teacher+=a.xpath("./text()").get().replace("","")
                    item['teachers']=teacher
                elif (t=="org_con"):
                    item['school']=i.xpath("./span/text()").get()
                else:
                    item['stu_num']= str.strip(str(i.xpath("./text()").get()))
            if (item.get("teachers")==None):
                item["teachers"]="Unknown"
            if (item.get("school")==None):
                item["school"]="Unknown"
            if (item.get("stu_num")==None):
                item["stu_num"]="Unknown"
            if (item['name']):
                cnt+=1; 
                yield(item)
        print("cnt=",cnt)
        print("url=",kwargs["url"])
        # np=responce.xpath("/html/body/div[4]/div[1]/div[7]/div[2]/div/a[last()]/@href").get();
        if (cnt==0):
            print("need restart")
            yield responce.follow(kwargs["url"],callback=self.parse,dont_filter=True,cb_kwargs=kwargs)