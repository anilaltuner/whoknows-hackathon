import requests
from config import config


class Jina:
    def __init__(self):
        self.scrape_url_template = "https://r.jina.ai/{}"
        self.scrape_headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {config.JINA_API_KEY}',
            'X-With-Images-Summary': 'true',
            "X-Timeout": '5'
        }
        self.jina_tokens = config.JINA_BACKUP_TOKENS if hasattr(config, 'JINA_BACKUP_TOKENS') else []

    def scrape(self, url):
        scrape_url = self.scrape_url_template.format(url)
        try:
            scrape_response = requests.get(scrape_url, headers=self.scrape_headers, timeout=10)
        except requests.exceptions.Timeout:
            return None

        scraped_content = scrape_response.json()
        if scraped_content.get("name", "Unknown error") == "InsufficientBalanceError":
            if self.jina_tokens:
                self.scrape_headers["Authorization"] = f"Bearer {self.jina_tokens.pop()}"
            else:
                return None

        if scraped_content["code"] != 200:
            print(f"Failed to scrape content from {url} for reason: {scraped_content.get('name', 'Unknown error')}")
            return None

        return scraped_content["data"]
