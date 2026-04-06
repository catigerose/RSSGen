from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from platform import system
from time import sleep

import feedparser
import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from pytz import timezone
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

# 统一时区，避免不同脚本各自处理时间导致 RSS 时间不一致。
SHANGHAI_TZ = timezone("Asia/Shanghai")

# 使用 Path 统一处理目录，兼容 Windows 与 Linux。
PROJECT_ROOT = Path(__file__).resolve().parent
if system() == "Linux":
    WORK_DIR = PROJECT_ROOT
elif system() == "Windows":
    WORK_DIR = PROJECT_ROOT
else:
    print("warning: unsupported platform, fallback to project directory")
    WORK_DIR = PROJECT_ROOT

FEEDS_DIR = WORK_DIR / "feeds"
FEEDS_DIR.mkdir(parents=True, exist_ok=True)
FEEDS_BASE_URL = "http://rss.catigerose.tech/feeds/"

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    )
}

DYNAMIC_BROWSER_ARGUMENTS = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--disable-extensions",
    "--no-first-run",
    "--no-default-browser-check",
    "--window-size=1920,1080",
]


@dataclass
class FeedEntry:
    title: str
    content: str
    link: str
    guid: str
    updated: datetime | str
    published: datetime | str


def get_soup(url, is_dynamic=False, timeout=10, sleep_seconds=1.0):
    """抓取网页并返回 BeautifulSoup 对象。

    `is_dynamic=True` 时使用 Selenium 处理依赖前端渲染的页面。
    """
    if is_dynamic:
        last_exception = None
        for headless_argument in ("--headless=new", "--headless"):
            for _ in range(2):
                options = Options()
                options.add_argument(headless_argument)
                for argument in DYNAMIC_BROWSER_ARGUMENTS:
                    options.add_argument(argument)
                options.add_argument(f"--user-agent={DEFAULT_HEADERS['User-Agent']}")
                options.add_experimental_option(
                    "prefs", {"intl.accept_languages": "zh-CN,en,en_US"}
                )

                driver = None
                try:
                    driver = Chrome(options=options)
                    driver.get(url)
                    sleep(sleep_seconds)
                    page_source = driver.page_source
                    return BeautifulSoup(page_source, features="lxml")
                except (SessionNotCreatedException, WebDriverException) as exc:
                    last_exception = exc
                    sleep(1)
                finally:
                    if driver is not None:
                        driver.quit()

        raise last_exception

    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    sleep(sleep_seconds)
    return BeautifulSoup(response.text, features="lxml")


def build_feed(
    website_url,
    feed_title,
    feed_description,
    feed_url,
    entries,
    start_index=0,
):
    """根据传入的 entry 列表构建 Atom feed。"""
    feed_generator = FeedGenerator()
    feed_generator.title(feed_title)
    feed_generator.updated(datetime.now(SHANGHAI_TZ))
    feed_generator.id(website_url)
    feed_generator.link(href=website_url, rel="alternate")
    feed_generator.link(rel="self", type="application/atom+xml", href=feed_url)
    feed_generator.author(name="catigerose", email="catigerose@gmail.com")
    feed_generator.subtitle(feed_description)

    for entry in entries[start_index:]:
        feed_entry = feed_generator.add_entry()
        feed_entry.title(entry.title)
        feed_entry.content(entry.content, type="html")
        feed_entry.link(href=entry.link)
        feed_entry.id(entry.guid)
        feed_entry.updated(entry.updated)
        feed_entry.published(entry.published)

    return feed_generator


def get_entries(feed_path):
    """读取已有 feed，返回 FeedEntry 列表。

    文件不存在时直接返回空列表，方便首次生成时复用同一套流程。
    """
    feed_file = Path(feed_path)
    if not feed_file.exists():
        return []

    parsed_feed = feedparser.parse(str(feed_file))
    entries = []
    existing_entries = list(parsed_feed.entries)
    existing_entries.reverse()
    for entry in existing_entries:
        content_value = ""
        if getattr(entry, "content", None):
            content_value = entry.content[0].value
        elif getattr(entry, "summary", None):
            content_value = entry.summary

        entries.append(
            FeedEntry(
                title=getattr(entry, "title", ""),
                content=content_value,
                link=getattr(entry, "link", ""),
                guid=getattr(entry, "guid", getattr(entry, "id", "")),
                updated=getattr(entry, "updated", getattr(entry, "published", "")),
                published=getattr(entry, "published", getattr(entry, "updated", "")),
            )
        )

    return entries


def get_json(url, timeout=10):
    """请求 JSON 接口并返回解析结果。"""
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.json()


def append_entry(
    entries,
    *,
    title,
    content,
    link,
    guid=None,
    updated=None,
    published=None,
):
    """向 FeedEntry 列表中追加一条记录。"""
    current_time = datetime.now(SHANGHAI_TZ)
    entries.append(
        FeedEntry(
            title=title,
            content=content,
            link=link,
            guid=guid or link,
            updated=updated or current_time,
            published=published or current_time,
        )
    )


def persist_feed(
    *,
    website_url,
    feed_title,
    feed_description,
    feed_name,
    entries,
    existing_entry_count,
    added_entry_count,
):
    """将采集结果写入 feed 文件。"""
    feed_path = FEEDS_DIR / feed_name
    feed_url = FEEDS_BASE_URL + feed_name
    start_index = min(existing_entry_count, added_entry_count)
    feed_generator = build_feed(
        website_url,
        feed_title,
        feed_description,
        feed_url,
        entries,
        start_index,
    )
    feed_generator.atom_file(str(feed_path))
    return feed_path
