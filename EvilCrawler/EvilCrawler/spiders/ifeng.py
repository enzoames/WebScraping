import scrapy
import os
import sys

# lib_path = os.path.realpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../', 'server'))
# if lib_path not in sys.path:
#     sys.path[0:0] = [lib_path]
# from mongo import save_mongo, check_mongo

class iFengSpider(scrapy.Spider):
    name = 'ifeng_spider'  # name must be unique
    start_urls = ['http://finance.ifeng.com/']

    def parse(self, response):
        url_list = response.css('div.box_01 > div > div.box_hot01.clearfix > h2 > a::attr(href)').extract()
        # more urls
        temp_urls = response.css('div.box_01 > div > div.box_hot01.clearfix > div > a::attr(href)').extract()

        temp2_urls = response.css('div.box_01 > div > div.box_hot01.clearfix > ul > li > a::attr(href)').extract()

        url_list = list(filter(lambda x: 'http://finance.ifeng.com/a/' in x, map(lambda x: x.strip(), temp_urls + temp2_urls + url_list)))

        for url in url_list:  # iterating through the list of URLs
            # print ("URL", url)
            print ('=============================================================')
            yield scrapy.Request(url=url, callback=self.parseSingleArticle)

    def parseSingleArticle(self, response):
        url = response.request.url  # grabs the url from the article

    #if check_mongo(url):

        single_article = {
            'url': url,
            'source': 'ifeng finance',
            'title': response.css('#artical_topic::text').extract_first(),
            'description': response.xpath("//meta[@name='description']").extract()[0].strip('<meta name="description" content="').strip('">'),
            'content': " ", # NEEDS CONTENT !
            # strip removes empty space
            'datetime': response.css('#artical_sth > p > span.ss01::text').extract_first(),
            'keywords': response.xpath("//meta[@name='keywords']").extract()[0].strip('<meta name="description" content="').strip('">'),
        }

     #   save_mongo(single_article, url)
        yield single_article
    #else:
    #    print('this page is already crawled')


# /html/body/meta[2]/text()

# #artical_topic

# #artical_sth > p > span.ss01

# /html/body/meta[2]

# /html/body/meta[2]

# body > meta:nth-child(15)

# /html/body/meta[2]