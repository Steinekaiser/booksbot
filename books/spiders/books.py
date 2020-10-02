# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["www.thalia.de"]
    start_urls = [
        'https://www.thalia.de/kategorie/lego-star-wars-11061/?allayout=FLAT',
    ]

    def parse(self, response):
        for book_url in response.css("li.suchergebnis > a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(book_url), callback=self.parse_book_page)
        next_page = response.css("li.next > a ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_book_page(self, response):
        item = {}
        product = response.css("main.artikel_uebersicht")
        item["title"] = product.css("h1 ::text").extract_first()
   #     item['category'] = response.xpath(
   #         "//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()"
   #     ).extract_first()
   #     item['description'] = response.xpath(
   #         "//div[@id='product_description']/following-sibling::p/text()"
   #     ).extract_first()
        item['price'] = response.css('section.artikel-infos ::attr(data-price-brutto)').extract_first()
        yield item
