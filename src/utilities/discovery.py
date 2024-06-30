import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple

from config import config
from utilities.jina import Jina
from utilities.serper import Serper


class Discovery:
    def __init__(self):
        self.google_search = Serper()
        self.jina_scraper = Jina()

    @staticmethod
    def remove_urls(text: str) -> str:
        url_pattern = re.compile(r'https?://\S+')
        return url_pattern.sub('', text)

    def query(self, query_str: str) -> Tuple[List[Dict[str, str]], List[str], List[Dict[str, str]]]:
        results = []
        images = []
        sources = []
        metadatas, urls = self.google_search.search(query_str)

        def scrape_url(url):
            scraped_content = self.jina_scraper.scrape(url)
            if scraped_content:
                if len(scraped_content["content"].split()) > int(config.MIN_CONTENT_WORDS or 0) and \
                        config.EXCLUDED_DOMAIN not in scraped_content["title"]:
                    scraped_content["content"] = self.remove_urls(scraped_content["content"])
                    if config.DEBUG_MODE:
                        print(f"Scraped content from {url} successfully. Query: {query_str}")
                    return scraped_content
            return None

        with ThreadPoolExecutor(max_workers=config.MAX_THREADS) as executor:
            future_to_url = {executor.submit(scrape_url, url): url for url in urls[:config.MAX_RESULTS]}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    scraped_content = future.result()
                    if scraped_content:
                        results.append(scraped_content)
                        images += list(scraped_content["images"].values())[:2]
                        sources.append({"title": scraped_content["title"], "url": scraped_content["url"]})
                except Exception as exc:
                    print(f"{url} generated an exception: {exc}")
                finally:
                    time.sleep(float(config.SCRAPE_DELAY or 1))

        return results, images, sources
