"""Fields exported by the quotes spider."""

import scrapy


class QuoteItem(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    source_url = scrapy.Field()
