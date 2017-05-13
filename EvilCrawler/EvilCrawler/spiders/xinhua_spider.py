# Ames
import scrapy
import os
import sys
# lib_path = os.path.realpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../', 'server'))
# if lib_path not in sys.path:
#     sys.path[0:0] = [lib_path]
# from mongo import save_mongo, check_mongo

class XinhuaSpider(scrapy.Spider):

    name = 'xinspider'
    start_urls = ['http://www.xinhuanet.com/world/index.htm']

    def parse(self, response):
        url_list = response.css('div.partL > div > ul.dataList > li.clearfix > h3 > a::attr(href)').extract()
        self.title_list = response.css('div.partL > div > ul.dataList > li.clearfix > h3 > a::text').extract()
        self.description_list = response.css('div.partL > div > ul.dataList > li.clearfix > p::text').extract()
        self.img_src_list =  response.css('div.partL > div > ul.dataList > li.clearfix > i  > a > img::attr(src)').extract()
        self.img_src_list = list(map(lambda x: 'http://www.xinhuanet.com/world/' + x, self.img_src_list))
        self.article_count = 0

        print()

        for url in url_list[:7]:  # we only need the first seven articles
            print ('=============================================================')
            print ("\tSCRAPING THIS URL: ", url)
            yield scrapy.Request(url=url, callback=self.parseSingleArticle)

    def parseSingleArticle(self, response):

        url = response.request.url  # grabs the url from the article

    # if check_mongo(url):
        article_content = response.xpath('//*[@id="p-detail"]/p/text()').extract()
        article_content = ''.join(article_content)

        single_article = {
            'url': url,
            'source': 'Xinhua',
            'title': self.title_list[self.article_count],
            'description': self.description_list[self.article_count],
            'image_src': self.img_src_list[self.article_count],
            'content': article_content,
            'datetime': response.css('div.h-p3.clearfix > div > div.h-info > span.h-time::text').extract_first().strip(),
            'keywords': response.xpath('/html/head/meta[9]/@content').extract_first().strip()
        }
        # save_mongo(single_article, url)
        self.article_count+=1
        yield single_article

        # else:
        #     print('this page is already crawled')

