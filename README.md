# housing-price-checker

```
scrapy crawl xplist -o houselist.csv
```




```
In Settings.py

# FEED_EXPORT_ENCODING='UTF-8'
FEED_EXPORT_ENCODING='gb18030'
```


# Scrapy shell

(https://docs.scrapy.org/en/latest/topics/shell.html)
```
scrapy shell <file|url>
response.xpath(XPATH)
```

```
    def parse(self, response):
        # We want to inspect one specific response.
        if ".org" in response.url:
            from scrapy.shell import inspect_response
            inspect_response(response, self)

        # Rest of parsing code.
```