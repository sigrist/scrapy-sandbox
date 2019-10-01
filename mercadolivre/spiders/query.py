import scrapy
from scrapy.loader import ItemLoader
from mercadolivre.items import MercadolivreItem

class QuerySpider(scrapy.Spider):
    name = "query"

    def __init__(self, query='', **kwargs):
        self.url = f"https://lista.mercadolivre.com.br/{query}"
        super().__init__(**kwargs)

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        for item in response.css('li.results-item'):
            il = ItemLoader(item=MercadolivreItem(), selector=item)

            il.add_css('sourceId', 'div.rowItem::attr(id)')
            il.add_css('title', 'span.main-title::text')
            try:
                il.add_css('image_urls', 'div.image-content img::attr(src)')
            except:
                pass
            yield il.load_item()

        #next_page = response.css('#results-section > div.pagination__container > ul > li.andes-pagination__button.andes-pagination__button--next > a::attr(href)').get() 
        #if next_page is not None:            
        #    yield response.follow(next_page, callback=self.parse)

        