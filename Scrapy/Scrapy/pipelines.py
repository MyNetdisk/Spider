# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
from Scrapy.items import DoubanMovieItem
from Scrapy.items import DoubanBookItem
from scrapy.exporters import JsonItemExporter


class ScrapyPipeline:
    def process_item(self, item, spider):
        return item


class JsonWriterMovieItemPipeline:
    """导出电影JSON文件"""

    def __init__(self):
        self.file = open("douban_movie.json", 'wb')
        self.exporter = JsonItemExporter(
            self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MovieItemPipeline:
    """导出电影Excel文件"""

    def __init__(self) -> None:
        self.wb = openpyxl.Workbook()
        self.sheet = self.wb.active
        self.sheet.title = '豆瓣电影数据Top250'
        self.sheet.append(('名称', '评分', '名言'))

    def process_item(self, item: DoubanMovieItem, spider):
        self.sheet.append((item['title'], item['score'], item['motto']))
        return item

    def close_spider(self, spider):
        self.wb.save('豆瓣电影数据Top250.xlsx')


class JsonWriterBookItemPipeline:
    """导出读书JSON文件"""

    def __init__(self):
        self.file = open("douban_book.json", 'wb')
        self.exporter = JsonItemExporter(
            self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class BookItemPipeline:
    """导出读书Excel文件"""

    def __init__(self) -> None:
        self.wb = openpyxl.Workbook()
        self.sheet = self.wb.active
        self.sheet.title = '豆瓣读书数据Top250'
        self.sheet.append(('名称', '评分', '名言'))

    def process_item(self, item: DoubanBookItem, spider):
        self.sheet.append((item['title'], item['score'], item['motto']))
        return item

    def close_spider(self, spider):
        self.wb.save('豆瓣读书数据Top250.xlsx')
