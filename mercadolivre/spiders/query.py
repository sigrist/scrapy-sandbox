import scrapy

class QuerySpider(scrapy.Spider):
    name = "query"

    def __init__(self, query='', **kwargs):
        self.url = f"https://lista.mercadolivre.com.br/{query}"
        super().__init__(kwargs)

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        searchResults = response.css('li.results-item')
        for result in searchResults:
            img = result.css('img.lazy-load')
            src = ''
            if img:
                src = img.attrib['src']
            yield {
                'sourceId': result.css('div.rowItem::attr(id)').get(),
                'title': result.css('span.main-title::text').extract_first(),
                'image_urls': src,
                'files_urls': result.css('a.item__info-title').attrib['href']                
            }
                    

        next_page = response.css('#results-section > div.pagination__container > ul > li.andes-pagination__button.andes-pagination__button--next > a::attr(href)').get() 
        if next_page is not None:            
            yield response.follow(next_page, callback=self.parse)

        