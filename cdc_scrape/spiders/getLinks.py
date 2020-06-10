import scrapy

class LinksSpider(scrapy.Spider):
    name = "links"

    start_urls = [
        'https://www.cdc.gov/coronavirus/2019-ncov/whats-new-all.html'
    ]

    def parse(self, response):
        links = response.css('.list-bullet.feed-item-list > li > a::attr(href)').getall()
        filename = 'all-cdc-links.txt'
        with open(filename,'w') as f:
            f.write(','.join(links))