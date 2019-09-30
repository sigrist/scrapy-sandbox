from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from mercadolivre.spiders.query import QuerySpider
import getopt
import sys

options, args = getopt.getopt(sys.argv[1:], 'q:', ['query='])
query = ''
for opt, arg in options:
    if opt in ('-q', '--query'):
        query = arg


if query != '':
    s = get_project_settings()
    process = CrawlerProcess(s)
    process.crawl(QuerySpider, query=query)

    process.start()
else:
    print('Use go-spider.py -q item_to_search')