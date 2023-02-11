import os
import logging
import newspaper
import pandas as pd
from google_news_api import GoogleNews

logger = logging.getLogger(__name__)

class NewsScraper():
    def __init__(self, countries: list, dates: list, topics: list, data_path: str, proxies: list = None) -> None:
        self.__countries = countries
        self.__dates = dates
        self.__topics = topics
        self.__data_path = data_path
        self.__proxies = proxies
        self.__google_news_client = GoogleNews()

    def __fetch_links(self, from_: str, to_: str, query: str):
        try:
            response = self.__google_news_client.search(query = query, from_ = from_, to_ = to_)
            return response['entries']
        except Exception as error:
            if self.__proxies:
                self.__use_porxy(query=query, from_=from_, to_=to_)
            else:
                logger.error(msg=error, exc_info=True)

    def __use_porxy(self, from_: str, to_: str, query: str):
        logger.info(msg='using proxies.')

        for proxy in self.__proxies:
            try:
                response = self.__google_news_client.search(query=query, from_=from_, to_=to_, proxies=proxy)
                return response['entries']
            except Exception as error:
                logger.error(msg=error, exc_info=True)

    def __get_article(self, url: str):
        try:
            article = newspaper.Article(url=url,languge='en')
            article.download()
            article.parse()

            # logger.info(msg=f'article title: {article.title}')

            return {
                "title": str(article.title),
                "text": str(article.text),
                "published_date": str(article.publish_date)
            }

        except Exception as error:
            # logger.error(msg=error, exc_info=True)
            return None

    def start_scraping(self):
        for country in self.__countries:
            self.__google_news_client.country = country
            logger.info(msg=f"on country: {country}")

            for i in range(0, len(self.__dates), 2):
                links = [entry['link'] for query in self.__topics for entry in self.__fetch_links(self.__dates[i], self.__dates[i+1], query)]
                logger.info(msg=f"from: {self.__dates[i]}, to: {self.__dates[i+1]}, total links: {len(links)}")
                
                articles = list(map(self.__get_article, links))
                not_none_values = filter(None.__ne__, articles)
                articles = list(not_none_values)

                logger.info(msg=f"articles recieved:: {len(articles)}")
                if len(articles)>0:
                    pd.DataFrame(data=articles).to_csv(os.path.join(self.__data_path, f"{country}-{self.__dates[i]}-{self.__dates[i+1]}.csv"), index=False)