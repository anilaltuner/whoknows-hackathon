import json
import requests
from config import config


class Serper:
    def __init__(self):
        self.search_url = "https://google.serper.dev/shopping"
        self.search_headers = {
            'X-API-KEY': config.SERPER_API_KEY,
            'Content-Type': 'application/json'
        }

    def search(self, query):
        search_payload = json.dumps({"q": query, "location": "United States"})
        search_response = requests.post(self.search_url, headers=self.search_headers, data=search_payload)
        search_data = search_response.json()
        metadatas = [result for result in search_data.get('shopping', [])]
        urls = [meta['link'] for meta in metadatas]
        return metadatas, urls
