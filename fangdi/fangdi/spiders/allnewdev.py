import scrapy
from scrapy_splash import SplashRequest
from fangdi.items import new_development
import re
import json

# http://www.fangdi.com.cn/service/freshHouse/getHosueList.action

path = 'http://www.fangdi.com.cn'

class AllnewdevSpider(scrapy.Spider):
    name = 'allnewdev'
    allowed_domains = ['fangdi.com.cn']
    start_urls = ['http://www.fangdi.com.cn/new_house/new_house_list.html']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, 
                args={'wait': 1}
            )

    def parse(self, response):
        with open(f'{self.name}.html', 'w') as f:
            f.write(response.body.decode('utf8'))

        # DEBUG CODE
        from scrapy.shell import inspect_response
        inspect_response(response, self)
        
        rx = re.compile(r"[a-f0-9]{10,}")

        for each in response.xpath("//tr[@class='default_row_tr']"):
            item = new_development()
            # status = scrapy.Field() 
            # project_name = scrapy.Field()
            # project_address = scrapy.Field()
            # total_units = scrapy.Field()
            # total_area = scrapy.Field()
            # area = scrapy.Field()
            cells = each.xpath('td')

            item['status'] = cells[0].xpath('text()').extract_first()
            item['project_name'] = cells[1].xpath('a/text()').extract_first()
            item['project_address'] = cells[2].xpath('text()').extract_first()
            item['total_units'] = cells[3].xpath('text()').extract_first()
            item['total_area'] = cells[4].xpath('text()').extract_first()
            item['area'] = cells[5].xpath('text()').extract_first()

            houseDetail = cells[1].xpath('a/@onclick').extract_first()
            houseDetail = rx.search(houseDetail)[0]
            detail_url = f'http://www.fangdi.com.cn/new_house/new_house_detail.html?project_id={houseDetail}'
            item['detail_url'] = detail_url

            yield item

            

class SplashPostHouseList(scrapy.Spider):
    name = "gethouselist"
    allowed_domains = ['fangdi.com.cn']
    start_urls = ['http://www.fangdi.com.cn/new_house/new_house_list.html']

    lua_script = """
    function main(splash, args)
        assert(splash:go{
            splash.args.url,
            http_method=splash.args.http_method,
            body=splash.args.body,
        })
        assert(splash:wait(0.5))
        return {
            html = splash:html(),
        }
        end
    """
    post_data = {
        'address': "",
        'currentPage': 1,
        'dicAvgpriceID': "",
        'dicPositionID': "",
        'dicRegionID': "",
        'districtID': "",
        'houseAreaID': "",
        'houseTypeID': "",
        'openingID': "",
        'projectName': "",
        'stateID': ""
    }

    # http://www.fangdi.com.cn/service/freshHouse/getHosueList.action
    
    def start_requests(self):
   
        url = path + '/service/freshHouse/getHosueList.action'
        yield SplashRequest(url, self.parse, 
            endpoint='execute',
            #endpoint='render.json',
            magic_response=True,
            meta={'handle_httpstatus_all': True},
            args={
                'wait': 1,
                'headers': {
                    'contentType': 'application/x-www-form-urlencoded;charset=utf-8',
                    'referer'
                },
                'lua_source': self.lua_script, 
                'http_method': 'POST', 
                'body': json.dumps(self.post_data)
                }
        )
    
    def parse(self, response):
        with open(f'{self.name}.html', 'w') as f:
            f.write(response.body.decode('utf8'))

        # DEBUG CODE
        from scrapy.shell import inspect_response
        inspect_response(response, self)
        
        rx = re.compile(r"[a-f0-9]{10,}")

        for each in response.xpath("//tr[@class='default_row_tr']"):
            item = new_development()
            # status = scrapy.Field() 
            # project_name = scrapy.Field()
            # project_address = scrapy.Field()
            # total_units = scrapy.Field()
            # total_area = scrapy.Field()
            # area = scrapy.Field()
            cells = each.xpath('td')

            item['status'] = cells[0].xpath('text()').extract_first()
            item['project_name'] = cells[1].xpath('a/text()').extract_first()
            item['project_address'] = cells[2].xpath('text()').extract_first()
            item['total_units'] = cells[3].xpath('text()').extract_first()
            item['total_area'] = cells[4].xpath('text()').extract_first()
            item['area'] = cells[5].xpath('text()').extract_first()

            houseDetail = cells[1].xpath('a/@onclick').extract_first()
            houseDetail = rx.search(houseDetail)[0]
            detail_url = f'http://www.fangdi.com.cn/new_house/new_house_detail.html?project_id={houseDetail}'
            item['detail_url'] = detail_url

            yield item

            