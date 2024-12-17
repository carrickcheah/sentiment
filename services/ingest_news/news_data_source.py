"""
Optimized NewsDataSource class for polling and producing news data.
"""
from time import sleep
from typing import Optional

from news_downloader import NewsDownloader
from quixstreams.sources.base import StatefulSource

class NewsDataSource(StatefulSource):
    """
    News data source that polls news periodically, processes it, and produces messages.
    """
    def __init__(self, news_downloader: NewsDownloader, polling_interval_sec: Optional[int] = 10):
        super().__init__(name='news_data_source')
        self.news_downloader = news_downloader
        self.polling_interval_sec = polling_interval_sec

    def run(self):
        last_published_at = self.state.get('last_published_at', None)
        while self.running:
            news = [item for item in self.news_downloader.get_news() if last_published_at is None or item.published_at > last_published_at]
            for news_item in news:
                message = self.serialize(key='news', value=news_item.to_dict())
                self.produce(key=message.key, value=message.value)
            if news:
                last_published_at = news[-1].published_at
            self.state.set('last_published_at', last_published_at)
            self.flush()
            sleep(self.polling_interval_sec)
