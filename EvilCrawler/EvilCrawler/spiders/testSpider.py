from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import scrapy

class InstagramSpider(scrapy.Spider):
    name = 'instaSpy'  # Name of spider must be unique

    start_urls = ['http://www.instagram.com/enzoames/']  # Scraping from instagram account

    # This function will take care of obtaining the url for each image in instagram
    def parse(self, response):
        # Given the location of each href response.css returns a list containing every url for every image
        selectedURLS = response.css('section > main > article > div > div > div > a::attr(href)').extract()
        # Attaching the original url to each element of selectedURLS
        selectedURLS2 = map(lambda x: 'http://www.instagram.com' + x, selectedURLS)

        print ("================================================")
        print len(selectedURLS2)
        print selectedURLS2

        for url in selectedURLS2:  # Applies request function to every url in list
            yield scrapy.Request(url=url, callback=self.parseSinglePage)

    def parseSinglePage(self, response):

        url = response.request.url

        singleArticle = {
            'url': url,
            'source': 'Instagram',
            'title': response.xpath('//section/main/div/div/article/div/ul/li/h1/span/text()').extract_first().strip(),
        }

        yield singleArticle



        # // *[ @ id = "react-root"] / section / main / div / div / article / div[2] / ul / li[1] / h1 / span / text()



        # // *[ @ id = "react-root"] / section / main / article / div / div[1]

        # //*[@id="react-root"]/section/main/article/div/div[1]/div[1]

        # #react-root > section > main > article > div > div._nljxa > div:nth-child(1) > a:nth-child(1)

        # #react-root > section > main > article > div > div._nljxa > div:nth-child(1) > a:nth-child(1)

        # #react-root > section > main > article > div > div._nljxa > div:nth-child(1)

        # #react-root > section > main > article > div > div._nljxa > div:nth-child(1) > a:nth-child(1)

        # //*[@id="react-root"]/section/main/article/div/div[1]

        # #react-root > section > main > div > div > article > div._es1du._rgrbt > ul > li:nth-child(1) > h1 > span
