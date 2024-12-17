"""
Optimized NewsDownloader and News class for fetching and parsing news from Cryptopanic API.
"""
from datetime import datetime
from typing import List, Tuple

import requests
from loguru import logger
from pydantic import BaseModel

class News(BaseModel):
    """
    Data model for the news.
    """
    title: str
    published_at: str
    source: str

    def to_dict(self) -> dict:
        return {
            **self.model_dump(),
            'timestamp_ms': int(
                datetime.fromisoformat(self.published_at.replace('Z', '+00:00')).timestamp() * 1000
            ),
        }

class NewsDownloader:
    """
    Downloads news from the Cryptopanic API.
    """
    URL = 'https://cryptopanic.com/api/free/v1/posts/'

    def __init__(self, cryptopanic_api_key: str):
        self.cryptopanic_api_key = cryptopanic_api_key

    def get_news(self) -> List[News]:
        news, url = [], f"{self.URL}?auth_token={self.cryptopanic_api_key}"
        while True:
            batch_of_news, next_url = self._get_batch_of_news(url)
            news += batch_of_news
            logger.debug(f'Fetched {len(batch_of_news)} news items')
            if not batch_of_news or not next_url:
                break
            url = next_url
        news.sort(key=lambda x: x.published_at)
        return news

    def _get_batch_of_news(self, url: str) -> Tuple[List[News], str]:
        response = requests.get(url)
        try:
            response = response.json()
        except Exception as e:
            logger.error(f'Error parsing response: {e}')
            from time import sleep
            sleep(1)
            return [], ''

        news = [
            News(
                title=post['title'],
                published_at=post['published_at'],
                source=post['domain']
            )
            for post in response['results']
        ]
        return news, response.get('next')

if __name__ == '__main__':
    from config import cryptopanic_config

    news_downloader = NewsDownloader(cryptopanic_api_key=cryptopanic_config.api_key)
    news = news_downloader.get_news()
    logger.debug(f'Fetched {len(news)} news items')
    breakpoint()
