import scrapy
from xiaopangSpider.items import houseItem
import re
from urllib.parse import urlparse, parse_qs



class XplistSpider(scrapy.Spider):
    name = 'xplist'
    allowed_domains = ['ipangchina.com']
    start_urls = ['http://www.ipangchina.com/index.php?caid=2&ccid51=5002&addno=1']
    page_url = None

    def parse(self, response):
        # //div[@class=houselist]
        # items = []
        
        # DEBUG INSPECT
        # scrapy.shell.inspect_response(response, self)

        for each in response.xpath("//div[@class='houselist']"):
            item = houseItem()

            # div class="info" 
            info  = each.xpath("div[@class='info']")
            item['name'] = info.xpath("h3/a/span/text()").extract()[0].strip()
            item['url'] = info.xpath("h3/a/@href").extract()[0].strip()
            item['listType'] = info.xpath("h3/i/text()").extract()[0].strip()

            item['area'] = re.sub(r'[\W\[\]]', '', info.xpath("p[1]/text()").extract()[0])
            item['address'] = info.xpath("p[1]/span/text()").extract()[0].strip()
            item['mapLink'] = info.xpath("p[1]/a/@href").extract()[0].strip()
            mapParts = parse_qs(urlparse(item['mapLink']).fragment)
            item['coordinates']=f"{mapParts['lng'][0]},{mapParts['lat'][0]}"
            
            item['tags'] = info.xpath("p[@class='tags']/span/text()").extract()
            
            # div class='other'
            other = each.xpath("div[@class='other']")
            item['avg_price'] = other.xpath("p[1]/a//text()").extract()[0].strip()
            item['telephone'] = other.xpath("p[@class='tel']/span/text()").extract()[0].strip()

            yield item
        
        for atag in response.xpath("//a[@class='p_redirect']"):
            url = atag.xpath("@href").extract()[0]
            text = atag.xpath("text()").extract()[0]
            # if text == '>>':
            #     # next_url = url
            #     yield scrapy.Request(url, self.parse)
        
