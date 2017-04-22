# WebScraping
Web Scraping/Crawling using Scrapy Framework

## Purpose

    The spiders contained in this repo were created by me as part of my internship
    at Alpine Capital Advisors. The spiders are currently being used for a larger
    project involving Machine Learning and Natural Language Processing.

### Explanation of built in Scrapy python files

   **Settings.py**
    Inside EvilCrawler/settings.py you can do custom things. Adding time delays between pages that 
    your grabbing information from. Also, you can set proxy server ip-addresses and not your
    own ip-address. Set your Spider name

   **Pipeline.py**
    Where you want to display/save your data - database such as mysql, mongo, etc

   **items.py**
    Dictionary or array of items that you can pass to other files in your project. Managing 
    your scrapped items. You can pass the elements that are inside items.py to pipeline.py
    which then can be saved in a database.

