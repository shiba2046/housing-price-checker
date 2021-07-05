import scrapy
from fangdi.items import houseItem
from scrapy_splash import SplashRequest


class NewdevSpider(scrapy.Spider):
    name = 'newdev'
    allowed_domains = ['fangdi.com.cn']
    start_urls = ['http://www.fangdi.com.cn/new_house/new_house_jjswlpgs.html']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, 
                args={'wait': 0.5}
            )

    def parse(self, response):
        with open('newdev.html', 'w') as f:
            f.write(response.body.decode('utf8'))

        # /html/body/div[3]/div/div[3]/div/div/ul[1]
        for each in response.xpath("//ul[@class='today_trade_info_item ring_item house_resouce_item clearfix']"):
            item = houseItem()
                # project_name = scrapy.Field()
                # area = scrapy.Field()
                # license_no = scrapy.Field()
                # sales_office_address = scrapy.Field()
                # start_date = scrapy.Field()
                # end_date = scrapy.Field()
                # telephone = scrapy.Field()
                # authority_telephone = scrapy.Field()
            item['project_name'] = each.xpath("li[@class='same_width_one']/span/text()").extract_first()
            item['area'] = each.xpath("li[@class='same_width_two']/span/text()").extract_first()
            item['license_no'] = each.xpath("li[@class='same_width_three']/span/text()").extract_first()
            item['sales_office_address'] = each.xpath("li[@class='same_width_four']/span/text()").extract_first()
            dates = each.xpath("li[@class='same_width_five']/span/text()").extract()
            item['start_date'] = dates[0]
            item['end_date'] = dates[1]
            item['telephone'] = each.xpath("li[@class='same_width_six']/span/text()").extract_first()
            item['authority_telephone'] = each.xpath("li[@class='same_width_seven']/span/text()").extract_first()
            
            # location.href=""+path+"/new_house/new_house_detail.html?project_id="+projectid;
            yield item