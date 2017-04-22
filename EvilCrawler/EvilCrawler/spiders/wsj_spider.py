""" 
Scraping Wall Street Journal website for articles related to finance and investing. (Chinese)

Requirements:  pip install scrapy
Terminal Command: scrapy crawl wsjspider -o wsj.json

"""

import scrapy

class WSJSpider(scrapy.Spider):
    name = 'wsjspider'
    start_url = 'http://cn.wsj.com/gb/'

    def parse(self, response):

        # extract the spotlight article's url
        url_spotlight = response.css('div.wsj-list.FP_LEAD_1.LS-SINGLE-SPOTLIGHT-SEVEN.rule-bottom.column > div'
                                     ' > div.wsj-card-body.clearfix.no-flow > h3 > a::attr(href)')
        # url list for the rest of the articles in the website, (total of 6)
        url_list = response.css('div.wsj-list.FP_LEAD_1.LS-SINGLE-SPOTLIGHT-SEVEN.rule-right.column.col5 > div'
                                     ' > div.wsj-card-body.clearfix > h3 > a::attr(href)')
        complete_list = url_spotlight + url_list
        complete_list = map(lambda x: 'http://cn.wsj.com/gb/' + x, complete_list)

        for url in complete_list[:1]:
            print ("============================================================")
            yield scrapy.Request(url=url, callback=self.parseSingleArticle)

    def parseSingleArticle(self, response):
        url = response.request.url

        single_article = {
            'url' : url,
            'source' : 'Wall Street Journal',
            'title': response.css('.blkContainerSblk > h1::text').extract_first().strip(),
            # 'description': ,
            # 'image_small_src': ,
            # 'image_large_src': ,
            # 'content': ,
            # 'datetime': ,

        }

        yield single_article


# Home > div.wsj-page.at12units.sector > div.column > div.space-bottom.column >
# div.wsj-main-well.column.col8 > div:nth-child(1) > div > \
#                                     div.wsj-list.FP_LEAD_1.LS-SINGLE-SPOTLIGHT-SEVEN.balance.column.col8

# //*[@id="Home"]/div[1]/div[1]/div[3]/div[1]/div[1]/div/div[2]/div

# //*[@id="Home"]/div[1]/div[1]/div[3]/div[1]/div[1]/div/div[2]/div[1]/div/div[2]



# ARTICLES URLS

# module.LS-SECONDARY.wsj-card.clearfix.media-first.media-flow
# div.wsj-card-body.clearfix

# div.wsj-card-body.clearfix.no-flow

# div.wsj-card-body.clearfix.no-flow


#Home > div.wsj-page.at12units.sector > div.column > div.space-bottom.column > div.wsj-main-well.column.col8 > div:nth-child(1) > div > div.wsj-list.FP_LEAD_1.LS-SINGLE-SPOTLIGHT-SEVEN.balance.column.col8 > div.wsj-list.FP_LEAD_1.LS-SINGLE-SPOTLIGHT-SEVEN.rule-bottom.column > div


# 'div.wsj-list.FP_LEAD_1.LS-SINGLE-SPOTLIGHT-SEVEN.rule-bottom.column'
# 'div.wsj-list.FP_LEAD_1.LS-SINGLE-SPOTLIGHT-SEVEN.rule-right.column.col5'

