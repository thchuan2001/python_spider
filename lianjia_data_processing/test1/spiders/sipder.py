import scrapy
from scrapy.http import response
from test1.items import Test1Item
class mySpider(scrapy.spiders.Spider):
    name="bupt"
    allowed_domains=["bj.lianjia.com"]
    start_urls=["https://bj.fang.lianjia.com/loupan/"]
    def start_requests(self):
        for url in self.start_urls:
            for pg in range(1,23):
                yield scrapy.Request(url+"pg"+str(pg),callback=self.parse,cb_kwargs={"page_num":1})
    def parse(self,responce,**kwargs):
        self.logger.info(kwargs.get("page_num"))
        item=Test1Item()
        self.logger.info("==========================================")
        for each in responce.xpath("/html/body/div[3]/ul[2]/*"):
            item['name']=each.xpath("./div/div[1]/a/text()").get()
            item['pos1']=each.xpath("./div/div[2]/span[1]/text()").get()
            item['pos2']=each.xpath("./div/div[2]/span[2]/text()").get()
            item['pos3']=each.xpath("./div/div[2]/a/text()").get()
            item['room_num']=each.xpath("./div/a/span[1]/text()").get()
            item['size']=int(each.xpath("./div/div[3]/span/text()").get().split(" ")[1].split("-")[0].replace("㎡",""))
            s=each.xpath("./div/div[6]/div[1]/span[2]/text()").get()
            num=each.xpath("./div/div[6]/div[1]/span[1]/text()").get().split("-")[0]
            if "均价" in s:
                item["avg_price"]=int(num)
                item['total_price']=item["avg_price"]*item['size']/10000
            else :
                item["total_price"]=float(num)
                item['avg_price']=item["total_price"]//item['size']
            item['total_price']="{:.4f}".format(item['total_price'])
            if (item['name']):
                yield(item)

        np=responce.xpath("/html/body/div[4]/a[last()]/@href").get();
        # if (kwargs.get('page_num')!=5):
        #     yield responce.follow(np,callback=self.parse,cb_kwargs={"page_num":kwargs.get('page_num')+1})