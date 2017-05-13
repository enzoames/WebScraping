"""
Scrapy spider to obtain news articles
"""

import scrapy

class NewsArticleSpider(scrapy.Spider):
    name = 'newsSpider'

    start_urls = ['http://www.washingtonexaminer.com/section/news']
