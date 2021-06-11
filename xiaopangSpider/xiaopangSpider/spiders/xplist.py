import scrapy
from xiaopangSpider.items import houseItem
import re

class XplistSpider(scrapy.Spider):
    name = 'xplist'
    allowed_domains = ['ipangchina.com']
    start_urls = ['http://www.ipangchina.com/index.php?caid=2&ccid51=5002&addno=1']
    page_url = None

    def parse(self, response):
        # //div[@class=houselist]
        # items = []

        for each in response.xpath("//div[@class='houselist']"):
            item = houseItem()

            # div class="info" 
            info  = each.xpath("div[@class='info']")
            name = info.xpath("h3/a/span/text()").extract()
            url = info.xpath("h3/a/@href").extract()
            listType = info.xpath("h3/i/text()").extract()

            # /html/body/div[3]/div[5]/div[3]/div[2]/p[1]
            area = info.xpath("p[1]/text()").extract()
            address = info.xpath("p[1]/span/text()").extract()
            mapLink = info.xpath("p[1]/a/@href").extract()
            
            # /html/body/div[3]/div[5]/div[3]/div[2]/p[2]
            tags = info.xpath("p[@class='tags']/span/text()").extract()
            # print(name,listType, area, address, tags)
            


            # div class='other'
            other = each.xpath("div[@class='other']")
            avg_price = other.xpath("p[1]/a//text()").extract()
            telephone = other.xpath("p[@class='tel']/span/text()").extract()


            item['name'] = name[0].strip()
            item['address'] = address[0].strip()
            
            item['listType'] = listType[0].strip()
            item['area'] = re.sub(r'[\W\[\]]', '', area[0])
            item['tags'] = tags
            item['avg_price'] = avg_price[0].strip()
            item['telephone'] = telephone[0].strip()
  
            item['url'] = url[0].strip()
            item['mapLink'] = mapLink[0].strip()
            
            
            #items.append(item)
            yield item
        
        for atag in response.xpath("//a[@class='p_redirect']"):
            url = atag.xpath("/@href").extract()
            text = atag.xpath("//text()").extract()
            if text == '>>':
                next_url = url
        
            print(f'Next page url: {next_url}')

        # return items
