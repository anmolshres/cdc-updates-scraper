import scrapy
import html2text
import cld2
from datetime import datetime

now = datetime.now()
class PostsSpider(scrapy.Spider):
    linksFile = open('all-cdc-links.txt','r')

    name = "posts"
    start_urls = map(lambda link: 'https://www.cdc.gov/'+ link if link.startswith('https') == False else link,linksFile.read().split(','))

    def parse(self, response):
        url = response.url
        datetime_today = now.strftime("%B %d, %Y %H:%M:%S")
        syndicate_content = response.css('.syndicate').extract()[1] if len(response.css('.syndicate').extract()) > 1 else response.css('.syndicate').extract()[0]
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        date = response.css('span#last-reviewed-date::text').get()
        title = response.css('title::text').get() 
        text = converter.handle(syndicate_content)
        isReliable, textBytesFound, details = cld2.detect(text)
        language = details[0].language_name
        yield{
            'title':title,
            'source':'Centers for Disease Control and Prevention',
            'date':date,
            'url':url,
            'scraped': datetime_today,
            'classes':['Government'],
            'country':'United States of America',
            'municipality':'National',
            'language': language,
            'text': text
        }
