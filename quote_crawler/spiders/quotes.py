"""Crawl the practice site's quotes and follow pagination."""

import scrapy
from scrapy.http import HtmlResponse

from quote_crawler.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def __init__(self, max_pages="0", *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.max_pages = int(max_pages)
        except (TypeError, ValueError) as exc:
            raise ValueError("max_pages must be a non-negative integer") from exc
        if self.max_pages < 0:
            raise ValueError("max_pages must be a non-negative integer")

    def parse(self, response: HtmlResponse, page_number: int = 1):
        for quote in response.css("div.quote"):
            yield QuoteItem(
                text=quote.css("span.text::text").get(),
                author=quote.css("small.author::text").get(),
                tags=quote.css("div.tags a.tag::text").getall(),
                source_url=response.url,
            )

        next_page = response.css("li.next a::attr(href)").get()
        within_limit = self.max_pages == 0 or page_number < self.max_pages
        if next_page and within_limit:
            yield response.follow(
                next_page,
                callback=self.parse,
                cb_kwargs={"page_number": page_number + 1},
            )
