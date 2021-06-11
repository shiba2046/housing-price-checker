# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class houseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    address = scrapy.Field()
    listType = scrapy.Field()
    area = scrapy.Field()
    mapLink = scrapy.Field()
    developer = scrapy.Field()
    tags = scrapy.Field()
    avg_price = scrapy.Field()
    telephone = scrapy.Field()
