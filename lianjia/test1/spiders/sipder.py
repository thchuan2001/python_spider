import scrapy
from scrapy.http import response
from test1.items import Test1Item
py2hz={"dongcheng":"东城","xicheng":"西城","haidian":"海淀","chaoyang":"朝阳"}
class mySpider(scrapy.spiders.Spider):
    name="bupt"
    allowed_domains=["bj.lianjia.com"]
    start_urls=["https://bj.lianjia.com/ershoufang/dongcheng/",
                "https://bj.lianjia.com/ershoufang/xicheng/",
                "https://bj.lianjia.com/ershoufang/chaoyang/",
                "https://bj.lianjia.com/ershoufang/haidian/"]
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,callback=self.parse,cb_kwargs={"page_num":1})
    def parse(self,responce,**kwargs):
        self.logger.info(kwargs.get("page_num"))
        item=Test1Item()
        self.logger.info("==========================================")
        for each in responce.xpath("/html/body/div[4]/div[1]/ul/*"):
            item['district']=py2hz[responce.url.split("/")[4]]
            item['name']=each.xpath("./div[1]/div[1]/a/text()").get()
            item['total_price']=each.xpath("./div[1]/div[6]/div[1]/span/text()").get()+"万"
            item['unit_price']=each.xpath("./div[1]/div[6]/div[2]/span/text()").get()
            item['square']=each.xpath("./div[1]/div[3]/div/text()").get().split("|")[1]
            if (item['name']):
                yield(item)
        
        np=responce.xpath("/html/body/div[4]/div[1]/div[7]/div[2]/div/a[last()]/@href").get();
        if (kwargs.get('page_num')!=5):
            yield responce.follow(np,callback=self.parse,cb_kwargs={"page_num":kwargs.get('page_num')+1})