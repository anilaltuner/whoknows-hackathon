import os
from dotenv import load_dotenv
from typing import Dict, Any

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        load_dotenv()
        self._config: Dict[str, Any] = {

            'SERPER_API_KEY': os.getenv('SERPER_API_KEY'),
            'JINA_API_KEY': os.getenv('JINA_API_KEY'),
            'JINA_BACKUP_TOKENS': os.getenv('JINA_BACKUP_TOKENS', '').split(','),
            'API_HOST': os.getenv('API_HOST', '0.0.0.0'),
            'API_PORT': int(os.getenv('API_PORT', 8000)),
            'DEBUG_MODE': os.getenv('DEBUG_MODE', 'False').lower() == 'true',
            'MAX_RESULTS': int(os.getenv('MAX_RESULTS', 5)),
            'SCRAPE_DELAY': float(os.getenv('SCRAPE_DELAY', 1.0)),
            'MIN_CONTENT_WORDS': int(os.getenv('MIN_CONTENT_WORDS', 30)),
            'EXCLUDED_DOMAIN': os.getenv('EXCLUDED_DOMAIN', 'www.reddit.com/r'),
            'MISTRAL_API_KEY': os.getenv('MISTRAL_API_KEY'),
            'MISTRAL_MODEL': os.getenv('MISTRAL_MODEL'),
        }

    def __getattr__(self, name):
        return self._config.get(name)

    def validate(self):
        required_vars = ['SERPER_API_KEY', 'JINA_API_KEY', 'MISTRAL_API_KEY', 'MISTRAL_MODEL']
        missing = [var for var in required_vars if self._config.get(var) is None]
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")

config = Config()
config.validate()
