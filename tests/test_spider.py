from pathlib import Path

import pytest
from scrapy import Request
from scrapy.http import HtmlResponse

from quote_crawler.items import QuoteItem
from quote_crawler.spiders.quotes import QuotesSpider


@pytest.fixture
def response():
    body = (Path(__file__).parent / "fixtures" / "quotes.html").read_bytes()
    request = Request("https://quotes.toscrape.com/", cb_kwargs={"page_number": 1})
    return HtmlResponse(request.url, body=body, encoding="utf-8", request=request)


def test_extracts_items_and_follows_relative_pagination(response):
    spider = QuotesSpider()
    results = list(spider.parse(response))
    items = [result for result in results if isinstance(result, QuoteItem)]
    requests = [result for result in results if isinstance(result, Request)]

    assert len(items) == 2
    assert items[0]["text"].split() == ["A", "sample", "quotation."]
    assert items[0]["author"].strip() == "Sample Author"
    assert [tag.strip() for tag in items[0]["tags"]] == ["example", "learning"]
    assert items[0]["source_url"] == response.url
    assert items[1]["tags"] == []
    assert len(requests) == 1
    assert requests[0].url == "https://quotes.toscrape.com/page/2/"
    assert requests[0].cb_kwargs == {"page_number": 2}


def test_one_page_limit_stops_pagination(response):
    results = list(QuotesSpider(max_pages="1").parse(response))
    assert len(results) == 2
    assert all(isinstance(result, QuoteItem) for result in results)


def test_limit_is_applied_to_later_pages(response):
    spider = QuotesSpider(max_pages="2")
    assert any(isinstance(result, Request) for result in spider.parse(response))
    assert not any(
        isinstance(result, Request) for result in spider.parse(response, page_number=2)
    )


def test_last_page_does_not_schedule_another_request(response):
    last_page = response.replace(body=b'<div class="quote"><span class="text">Last.</span></div>')
    assert not any(isinstance(result, Request) for result in QuotesSpider().parse(last_page))


@pytest.mark.parametrize("value", ["-1", "abc", "1.5", ""])
def test_rejects_invalid_page_limit(value):
    with pytest.raises(ValueError, match="max_pages"):
        QuotesSpider(max_pages=value)
