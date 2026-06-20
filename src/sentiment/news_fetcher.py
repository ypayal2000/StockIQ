import feedparser
import pandas as pd


class NewsFetcher:

    def __init__(self):

        self.feeds = {
            "TCS.NS":
                "https://news.google.com/rss/search?q=TCS+stock",
            "INFY.NS":
                "https://news.google.com/rss/search?q=Infosys+stock",
            "RELIANCE.NS":
                "https://news.google.com/rss/search?q=Reliance+Industries+stock",
            "HDFCBANK.NS":
                "https://news.google.com/rss/search?q=HDFC+Bank+stock"
        }

    def fetch_news(self):

        all_news = []

        for symbol, feed_url in self.feeds.items():

            print(f"Fetching news for {symbol}")

            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:10]:

                all_news.append({
                    "symbol": symbol,
                    "headline": entry.title,
                    "published": entry.get(
                        "published",
                        None
                    ),
                    "source": "Google News"
                })

        return pd.DataFrame(all_news)


if __name__ == "__main__":

    fetcher = NewsFetcher()

    df = fetcher.fetch_news()

    print(df.head())

    print(
        f"\nTotal Articles: {len(df)}"
    )