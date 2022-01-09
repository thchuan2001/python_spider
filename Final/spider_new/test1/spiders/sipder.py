import scrapy
from scrapy.http import response
from test1.items import Test1Item
not_country=["World","High income","Upper middle income","Asia","Europe","Lower middle income","North America","European Union","South America","Africa","Oceania"]
class mySpider(scrapy.spiders.Spider):
    name="bupt"
    allowed_domains=["ourworldindata.org"]
    with open("./date.txt","r") as f:
        date=f.read()
    start_urls=["https://ourworldindata.org/explorers/coronavirus-data-explorer?tab=table&zoomToSelection=true&time=2021-12-{}&facet=none&uniformYAxis=0&pickerSort=asc&pickerMetric=total_cases&Metric=Confirmed+cases&Interval=New+per+day&Relative+to+Population=false&Color+by+test+positivity=false".format(date)]
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,callback=self.parse,cb_kwargs={"page_num":1})
    def parse(self,responce,**kwargs):
        #print (str(responce.text))
        item=Test1Item()
        print ("----------------------------")
        for each in responce.xpath("/html/body/main/div/div[3]/div/div[1]/div/table/tbody/*"):
            item['country']=each.xpath("./td[1]/text()").get()
            cases=str(each.xpath("./td[2]/text()").get())
            cases=cases.replace(",","")

            if (cases.find("million")!=-1):
                cases=cases.replace("million","")
                item['total_cases']=int((float(cases)*1000000))
            elif (cases.find("billion")!=-1):
                cases=cases.replace("billion","")
                item['total_cases']=int((float(cases)*1000000000))
            else :
                if (cases=="None"):
                    cases="0"
                item['total_cases']=int(cases)
            # item['name']=each.xpath("./div[1]/div[1]/a/text()").get()
            # item['total_price']=each.xpath("./div[1]/div[6]/div[1]/span/text()").get()+"万"
            # item['unit_price']=each.xpath("./div[1]/div[6]/div[2]/span/text()").get()
            # item['square']=each.xpath("./div[1]/div[3]/div/text()").get().split("|")[1]
            if (item['country']and item['country'] not in not_country):
                yield(item)
        
        # np=responce.xpath("/html/body/div[4]/div[1]/div[7]/div[2]/div/a[last()]/@href").get();
        # if (kwargs.get('page_num')!=5):
        #     yield responce.follow(np,callback=self.parse,cb_kwargs={"page_num":kwargs.get('page_num')+1})