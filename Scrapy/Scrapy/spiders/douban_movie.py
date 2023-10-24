import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from Scrapy.items import DoubanMovieItem


class DoubanMovieSpider(scrapy.Spider):
    name = "douban_movie"
    allowed_domains = ["movie.douban.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            "Scrapy.pipelines.MovieItemPipeline": 300,
            "Scrapy.pipelines.JsonWriterMovieItemPipeline": 800,
        }
    }

    def start_requests(self):
        for page in range(10):
            yield Request(url=f'https://movie.douban.com/top250?start={page*25}')

    def parse(self, response: HtmlResponse):
        sel = Selector(response)
        movie_items = sel.css('#content > div > div.article > ol > li')
        for movie_sel in movie_items:
            item = DoubanMovieItem()
            item['title'] = movie_sel.css('.title::text').extract_first()
            item['score'] = movie_sel.css('.rating_num::text').extract_first()
            item['motto'] = movie_sel.css('.inq::text').extract_first()
            yield item
        # 如果还要生成后续爬取的请求
        # hrefs = sel.css(
        #     '#content > div > div.article > div.paginator > a::attr("href")')
        # for href in hrefs:
        #     full_url = response.urljoin(href.extract())
        #     yield Request(url=full_url)
