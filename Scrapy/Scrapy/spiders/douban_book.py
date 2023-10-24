import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from Scrapy.items import DoubanBookItem


class DoubanBookSpider(scrapy.Spider):
    name = "douban_book"
    allowed_domains = ["book.douban.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            "Scrapy.pipelines.BookItemPipeline": 300,
            "Scrapy.pipelines.JsonWriterBookItemPipeline": 800,
        }
    }

    def start_requests(self):
        for page in range(10):
            yield Request(url=f'https://book.douban.com/top250?start={page*25}')

    def parse(self, response: HtmlResponse):
        sel = Selector(response)
        book_items = sel.css('#content>div>div.article>div.indent>table')
        for book_sel in book_items:
            item = DoubanBookItem()
            item['title'] = book_sel.css(
                'a[title]::attr(title)').extract_first()
            item['score'] = book_sel.css('.rating_nums::text').extract_first()
            item['motto'] = book_sel.css('.inq::text').extract_first()
            yield item
