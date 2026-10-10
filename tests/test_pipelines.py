import pytest
from scrapy.exceptions import DropItem

from quote_crawler.items import QuoteItem
from quote_crawler.pipelines import CleanQuotePipeline, DuplicatesPipeline


def test_cleans_whitespace_and_deduplicates_tags():
    item = QuoteItem(
        text="  Example\n  quote. ",
        author=" Sample\t Author ",
        tags=[" life ", "", "life", " learning\n"],
        source_url="https://quotes.toscrape.com/",
    )
    cleaned = CleanQuotePipeline().process_item(item)
    assert cleaned["text"] == "Example quote."
    assert cleaned["author"] == "Sample Author"
    assert cleaned["tags"] == ["life", "learning"]


@pytest.mark.parametrize(
    "item",
    [{"author": "Author"}, {"text": "Quote"}, {"text": " \n ", "author": "Author"}],
)
def test_drops_records_without_required_fields(item):
    with pytest.raises(DropItem):
        CleanQuotePipeline().process_item(item)


def test_same_quote_and_author_are_deduplicated_across_pages():
    pipeline = DuplicatesPipeline()
    first = {"text": "Quote", "author": "Author", "source_url": "/page/1/"}
    second = {**first, "source_url": "/page/2/"}
    assert pipeline.process_item(first) is first
    with pytest.raises(DropItem, match="Duplicate"):
        pipeline.process_item(second)
    other_author = {**first, "author": "Another Author"}
    assert pipeline.process_item(other_author) is other_author


def test_cleaning_happens_before_deduplication():
    cleaner = CleanQuotePipeline()
    deduplicator = DuplicatesPipeline()
    deduplicator.process_item(cleaner.process_item({"text": " Quote ", "author": "Author"}))
    with pytest.raises(DropItem):
        deduplicator.process_item(cleaner.process_item({"text": "Quote", "author": " Author "}))


def test_new_pipeline_has_independent_deduplication_state():
    item = {"text": "Quote", "author": "Author"}
    DuplicatesPipeline().process_item(item)
    assert DuplicatesPipeline().process_item(item) is item
