import scrapy

class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet/page-1"]

    def parse(self, response):
        items = response.css("div._Ud0k")
        for item in items:
            yield {
                "name": item.css('div.lsooF span::text').get(),
                "price": item.css('div.pY3d2 span::text').get(),
                "url": item.css('a').attrib['href'],
            }

        # Переход на следующую страницу
        next_page = response.css('a.next_page::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        else:
            # Попробуем вручную сформировать ссылку на следующую страницу
            current_page = response.url.split('-')[-1]
            try:
                next_page_number = int(current_page) + 1
                next_page_url = f"https://www.divan.ru/category/svet/page-{next_page_number}"
                yield response.follow(next_page_url, self.parse)
            except ValueError:
                # Если current_page не число, например, это первая страница
                next_page_url = "https://www.divan.ru/category/svet/page-2"
                yield response.follow(next_page_url, self.parse)