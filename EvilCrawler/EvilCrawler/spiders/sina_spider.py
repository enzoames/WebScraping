""" 
Scraping chinese website for articles related to finance and investing.

Requirements:  pip install scrapy
Terminal Command: scrapy crawl sinaspy -o sina.json

"""

import scrapy

class SinaSpider(scrapy.Spider):

    name = 'sinaspy'  # name must be unique

    start_urls = ['http://finance.sina.com.cn/stock/usstock/']  # URL from which we will crawl

    def parse(self, response):
        # Extracts all the article URL from SINA page
        url_list = response.css('div.txt > h2 > a::attr(href)').extract()
        # Extracts the corresponding description of each article
        self.description_list = response.css('div.txt > div.p > a::text').extract()
        # Extracts the corresponding image source of each article
        self.image_small_list = response.css('div.img > a > img::attr(src)').extract()
        # Keeps track of the number of articles as we crawl data
        self.articleCount = 0

        for url in url_list:  # iterating through the list of URLs
            #print ("URL", url)
            print ('=============================================================')
            yield scrapy.Request(url=url, callback=self.parseSingleArticle)


    def parseSingleArticle(self, response):  # This method will handle each url coming from parse
        # response parameter is an instance of textResponse.
        url = response.request.url  # grabs the url from the article
        # print (type(response))  # <class 'scrapy.http.response.html.HtmlResponse'>

        # In Sina page content is inside several p tags. this will return a list containing pieces of the article
        Article_content = response.xpath('//*[@id="artibody"]/p/text()').extract()

        Article_content = ''.join(Article_content)

        single_article = {
            'url': url,
            'source': 'Finance Sina',
            'title': response.css('.blkContainerSblk > h1::text').extract_first().strip(),
            'description': self.description_list[self.articleCount],
            'image_small_src': self.image_small_list[self.articleCount],
            'image_large_src': response.css('.blkContainerSblk > div.img_wrapper > img::attr(src)').extract_first(),
            'content': Article_content,
            # strip removes empty space
            'datetime': response.xpath('//*[@id="pub_date"]/text()').extract_first().strip(),
            'keywords': response.xpath('/html/head/meta[3]/@content').extract_first().strip(),
        }

        self.articleCount += 1

        yield single_article

