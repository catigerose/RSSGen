from datetime import date

from feed_funcs import FEEDS_DIR, append_entry, get_entries, get_soup, persist_feed


def build_day_prefix(target_day):
    return f"{target_day.year}{target_day.month:02d}/{target_day.day:02d}/"


def run():
    feed_title = "证券时报"
    feed_description = "证券时报电子版聚合。"
    feed_name = "zqsb.xml"
    website_url = "https://epaper.stcn.com/"

    entries = get_entries(FEEDS_DIR / feed_name)
    existing_guids = {entry.guid for entry in entries}
    existing_entry_count = len(entries)
    added_entry_count = 0

    day_prefix = build_day_prefix(date.today())
    index_url = "https://epaper.stcn.com/col/" + day_prefix + "node_A001.html"
    page_soup = get_soup(index_url)
    tree_node = page_soup.find("div", id="webtree")
    li_list = tree_node.find_all("li") if tree_node is not None else []

    for item in reversed(li_list):
        anchor = item.find("a")
        if anchor is None:
            continue

        news_url = "https://epaper.stcn.com/con/" + day_prefix + anchor["href"].split("/")[-1]
        if news_url in existing_guids:
            continue

        news_title = anchor.get_text(strip=True)
        append_entry(
            entries,
            title=news_title,
            content=news_title,
            link=news_url,
        )
        existing_guids.add(news_url)
        added_entry_count += 1

    persist_feed(
        website_url=website_url,
        feed_title=feed_title,
        feed_description=feed_description,
        feed_name=feed_name,
        entries=entries,
        existing_entry_count=existing_entry_count,
        added_entry_count=added_entry_count,
    )


if __name__ == "__main__":
    run()
