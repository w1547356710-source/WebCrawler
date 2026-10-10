"""Scrapy settings for quote_crawler."""

BOT_NAME = "quote_crawler"

SPIDER_MODULES = ["quote_crawler.spiders"]
NEWSPIDER_MODULE = "quote_crawler.spiders"

USER_AGENT = "quote_crawler/1.0 (Scrapy learning project)"
ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 4
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1.0
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.0
AUTOTHROTTLE_MAX_DELAY = 10.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
DOWNLOAD_TIMEOUT = 30
RETRY_ENABLED = True
RETRY_TIMES = 2

ITEM_PIPELINES = {
    "quote_crawler.pipelines.CleanQuotePipeline": 100,
    "quote_crawler.pipelines.DuplicatesPipeline": 200,
}

FEED_EXPORT_ENCODING = "utf-8"
FEED_EXPORT_FIELDS = ["text", "author", "tags", "source_url"]
LOG_LEVEL = "INFO"
TELNETCONSOLE_ENABLED = False
EXTENSIONS = {"scrapy.extensions.remote_control.RemoteControl": None}
