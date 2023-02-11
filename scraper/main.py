import os
import pandas as pd
from logger import Logger
from scraper.news_scraper import NewsScraper


def main():
    
    countries = ['US', 'UK', 'FR', 'CA', 'DE', 'IE', 'NZ', 'AU']
    dates = list(pd.date_range(start="2022-01-01", end="2022-07-31").astype('str'))
    topics = ['Business News', 'Sports News', 'Entertainment', 'Worlds News', 'Nation News',
                'Technology News', 'Entertainment News', 'Science News', 'Health News']

    proxy_path  = os.path.join(os.getcwd(), 'proxies', 'proxies.txt')
    proxies = None
    if os.path.exists(proxy_path):
        with open(proxy_path, 'r') as f:
            proxies = f.read().splitlines() 

    data_path = os.path.join(os.getcwd(), 'data')

    news_scrapper = NewsScraper(countries=countries, dates=dates, topics=topics, data_path=data_path, proxies=proxies)
    news_scrapper.start_scraping()

if __name__=='__main__':
    main()

