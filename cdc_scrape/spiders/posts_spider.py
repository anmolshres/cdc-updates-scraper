import scrapy
import html2text

class PostsSpider(scrapy.Spider):
    linksFile = open('all-cdc-links.txt','r')

    name = "posts"
    start_urls = map(lambda link: 'https://www.cdc.gov/'+ link if link.startswith('https') == False else link,linksFile.read().split(','))

    def parse(self, response):
        url = response.url
        syndicate_content = response.css('.syndicate').extract()[1] if len(response.css('.syndicate').extract()) > 1 else response.css('.syndicate').extract()[0]
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        date = response.css('span#last-reviewed-date::text').get()
        title = response.css('title::text').get() 
        yield{
            'title':title,
            'date':date,
            'url':url,
            'text':converter.handle(syndicate_content)
        }
