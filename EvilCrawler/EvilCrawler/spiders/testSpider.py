from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import scrapy

class InstagramSpider(scrapy.Spider):
    name = 'instaSpy'

    start_urls = ['http://www.instagram.com/enzoames/']

    def parse(self, response):

        #hxs = HtmlXPathSelector(response)  # a HTML selector
        # hsx will help to select different objects on the page

        selectedObjects = response.xpath('//*[@id="react-root"]/section/main/article/div/div/div/a/@href').extract()

        # urlList = response.css('div > a::attr(href)').extract()

        print "============================================================"
        print (type(selectedObjects))
        print selectedObjects

    #     for url in urlList:
    #         yield scrapy.Request(url=url,
    #                              callback=self.parseSinglePage)
    #
    # def parseSinglePage(self, response):
    #
    #     url = response.request.url
    #
    #     singleArticle = {
    #         'url': url,
    #         'source': 'Dongfangcaifu',
    #         'title': extract_with_css('.newsContent > h1::text'),
    #
    #     }
    #     yield singleArticle