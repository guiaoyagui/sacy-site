import feedparser
import json
from datetime import datetime

NASA_RSS_FEEDS = [
    "https://www.nasa.gov/rss/dyn/breaking_news.rss",
    "https://science.nasa.gov/news/rss.xml",
]

def coletar_artigos():
    artigos = []
    for feed_url in NASA_RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            artigos.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", ""),
                "summary": entry.get("summary", ""),
                "text": entry.get("summary", "")
            })
    with open("backend/data/articles.json", "w", encoding="utf-8") as f:
        json.dump(artigos, f, indent=2, ensure_ascii=False)
    print(f"✅ {len(artigos)} artigos coletados e salvos em backend/data/articles.json")

if __name__ == "__main__":
    coletar_artigos()
