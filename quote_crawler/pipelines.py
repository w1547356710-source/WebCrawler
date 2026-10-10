"""Clean and deduplicate items before Scrapy exports them."""

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


def clean_text(value: str | None) -> str:
    return " ".join((value or "").split())


class CleanQuotePipeline:
    def process_item(self, item):
        adapter = ItemAdapter(item)
        for field in ("text", "author"):
            adapter[field] = clean_text(adapter.get(field))
            if not adapter[field]:
                raise DropItem(f"Missing required field: {field}")

        tags = (clean_text(tag) for tag in adapter.get("tags", []))
        adapter["tags"] = list(dict.fromkeys(tag for tag in tags if tag))
        return item


class DuplicatesPipeline:
    """Deduplication state lasts for one crawler run."""

    def __init__(self):
        self.seen: set[tuple[str, str]] = set()

    def process_item(self, item):
        adapter = ItemAdapter(item)
        key = (adapter["text"], adapter["author"])
        if key in self.seen:
            raise DropItem("Duplicate quote and author")
        self.seen.add(key)
        return item
