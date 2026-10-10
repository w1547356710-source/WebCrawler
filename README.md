# Scrapy Python 爬虫项目

一个可以直接运行和扩展的 Scrapy 项目，使用 Python 3.10+、Scrapy 2.19.0。
示例爬虫采集 [Quotes to Scrape](https://quotes.toscrape.com/) 的名言、作者和标签。
该网站也是 [Scrapy 官方教程](https://docs.scrapy.org/en/latest/intro/tutorial.html) 使用的练习网站。

## 功能

- 自动跟随下一页，支持设置最大采集页数。
- 清理多余空白，丢弃缺少名言或作者的记录。
- 按名言和作者去重，去重范围是单次运行。
- 使用 Scrapy Feed Exports 导出 UTF-8 JSON、JSON Lines 或 CSV。
- 开启 robots.txt 检查、请求限速、自动节流、超时及重试。
- 附带离线测试和 GitHub Actions 工作流。

## 安装

从 GitHub 获取项目：

```bash
git clone https://github.com/w1547356710-source/WebCrawler.git
cd WebCrawler
```

在包含 `scrapy.cfg` 的项目根目录打开终端。

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m scrapy list
```

直接使用虚拟环境的 Python，无需修改 PowerShell 执行策略。

### macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m scrapy list
```

## 运行

Windows 上先采集两页（通常得到 20 条记录），保存为 JSON：

```powershell
.\.venv\Scripts\python.exe -m scrapy crawl quotes -a max_pages=2 -O data/quotes.json
```

采集所有分页并导出 CSV：

```powershell
.\.venv\Scripts\python.exe -m scrapy crawl quotes -O data/quotes.csv
```

导出 JSON Lines：

```powershell
.\.venv\Scripts\python.exe -m scrapy crawl quotes -a max_pages=2 -O data/quotes.jsonl
```

macOS/Linux 将命令中的 `.\.venv\Scripts\python.exe` 换成 `.venv/bin/python`。

`max_pages` 必须是非负整数：`0`（默认）表示采集所有分页；`1` 表示只采集首页。
`-O` 会覆盖已有输出文件；需要追加时使用 `-o data/quotes.jsonl`，避免追加普通 JSON。

导出字段：

| 字段 | 含义 |
| --- | --- |
| `text` | 名言正文 |
| `author` | 作者 |
| `tags` | 标签列表（CSV 中由 Scrapy 序列化） |
| `source_url` | 来源页面 URL |

## 项目结构

```text
scrapy-crawler/
├── scrapy.cfg
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── quote_crawler/
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders/
│       └── quotes.py
├── data/
├── tests/
│   ├── fixtures/
│   ├── test_spider.py
│   └── test_pipelines.py
└── .github/workflows/tests.yml
```

项目骨架由 `scrapy startproject quote_crawler` 生成。
`middlewares.py` 保留框架生成的扩展入口，默认不启用自定义中间件。

## 开发和测试

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m scrapy list
```

测试使用本地 HTML，覆盖字段解析、相对分页链接、页数限制、空白清洗和去重，无需联网。
GitHub Actions 在 Python 3.10 和 3.12 上运行测试，不访问目标网站。

## 扩展到其他网站

1. 在 `quote_crawler/spiders/` 中新建爬虫，设置独立的 `name`、`allowed_domains` 和 `start_urls`。
2. 根据页面 HTML 修改 CSS/XPath 选择器和分页逻辑。
3. 在 `items.py` 定义字段，在 `pipelines.py` 实现相应清洗规则，并在 `settings.py` 中注册。
4. 更新 `USER_AGENT`，填写真实的项目名称和联系信息。

默认配置允许每个域名同时处理一个请求，下载间隔为 1 秒，并启用自动节流。
失败请求最多重试两次，单个请求超时为 30 秒。可在 `settings.py` 调整。

## 保存到 GitHub

本项目的仓库为 [WebCrawler](https://github.com/w1547356710-source/WebCrawler)。
如果需要保存到自己的新仓库，先在 GitHub 新建空仓库，再在项目根目录执行（替换地址）：

```bash
git init -b main
git add .
git commit -m "Create Scrapy crawler project"
git remote add origin https://github.com/YOUR_USERNAME/scrapy-crawler.git
git push -u origin main
```

采集结果放在 `data/`，默认不提交到 GitHub。
