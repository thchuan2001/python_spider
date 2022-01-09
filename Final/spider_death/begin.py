from scrapy import cmdline
import os
for date in range(5,20):
    with open("./date.txt","w") as f:
        if (date<=9):
            f.write("0"+str(date))
        else :
            f.write(str(date))
    #cmdline.execute("scrapy crawl bupt".split())
    os.system("scrapy crawl bupt")