# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class houseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # pass
    project_name = scrapy.Field()
    area = scrapy.Field()
    license_no = scrapy.Field()
    sales_office_address = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    telephone = scrapy.Field()
    authority_telephone = scrapy.Field()

class new_development(scrapy.Item):
    status = scrapy.Field() 
    project_name = scrapy.Field()
    project_address = scrapy.Field()
    total_units = scrapy.Field()
    total_area = scrapy.Field()
    area = scrapy.Field()
    detail_url = scrapy.Field()