from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader

# 根据项目配置获取 CrawlerProcess 实例
process = CrawlerProcess(get_project_settings())

# 1.添加需要执行的爬虫(运行指定爬虫版本)
# process.crawl('douban_movie')
# process.crawl('douban_book')

# 2.获取 SpiderLoader 对象，进一步获取项目下所有的爬虫名称（运行所有爬虫版本）
spider_loader = SpiderLoader(get_project_settings())
# 添加需要执行的爬虫
for spidername in spider_loader.list():
    process.crawl(spidername)

# 执行
process.start()
