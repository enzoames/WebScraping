import scrapy
import os
import sys
lib_path = os.path.realpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../', 'server'))
if lib_path not in sys.path:
    sys.path[0:0] = [lib_path]
from mongo import save_mongo, check_mongo

class WSJSpider(scrapy.Spider):
    name = 'wsjspider'
    start_urls = ['http://cn.wsj.com/gb/index.asp']
 
    def __init__(self, *args, **kwargs):
       super(WSJSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # extract the spotlight article's url
        # populated from response.meta
        print("ABD")
        if response.url == 'http://cn.wsj.com/gb/index.asp':
            print("ABD222")
            url_spotlight = response.css('div.wsj-list.FP_LEAD_1.LS-SINGLE-SPOTLIGHT-SEVEN.rule-bottom.column > div'
                                         ' > div.wsj-card-body.clearfix.no-flow > h3 > a::attr(href)').extract()
            url_list = response.css('div.wsj-list.FP_LEAD_1.LS-SINGLE-SPOTLIGHT-SEVEN.rule-right.column.col5 > div'
                                    ' > div.wsj-card-body.clearfix > h3 > a::attr(href)').extract()

            complete_list = url_spotlight + url_list
            complete_list = list(map(lambda x: 'http://cn.wsj.com/gb/' + x, complete_list))
            print ("COMPLETE LIST:", complete_list)
            self.count = 1
            for url in complete_list:
                print ("============================================================")
                print ("SCRAPING THIS URL:", self.count, " " , url)
                yield scrapy.Request(url=url, callback=self.parse)

        else:
            url = response.request.url
            print('mongo requests')
            if check_mongo(url):
                article_content = response.css('#A > p::text').extract()
                article_content = ''.join(article_content)
                # if self.db.articles_data.find( { "url": url} ).count() == 0:
                single_article = {
                    'url': url,
                    'source': 'WSJ',
                    'title': response.xpath('//*[@id="article-contents"]/header/div/div/h1/text()').extract_first(),
                    'description': response.xpath('//*[@id="article-contents"]/header/div/div/h2/text()').extract_first(),
                    'image_src': response.css('div.image-container.responsive-media.loaded > img::attr(src)').extract_first(),
                    'content': article_content,
                    'datetime': response.css('#A > div.clearfix.byline-wrap > time::text').extract_first().strip(),
                    'keywords': response.xpath('/html/head/meta[33]/@content').extract_first(),
                }
                save_mongo(single_article, url)
                self.count+=1
                yield single_article
            else:
                print('this page is already crawled')
