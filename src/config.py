import os
from dotenv import load_dotenv
from typing import Dict, Any
import streamlit as st
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

            'SERPER_API_KEY': st.secrets['SERPER_API_KEY'],
            'JINA_API_KEY': st.secrets['JINA_API_KEY'],
            'JINA_BACKUP_TOKENS': st.secrets['JINA_BACKUP_TOKENS'],
            'MAX_RESULTS': int(st.secrets['MAX_RESULTS']),
            'MAX_THREADS': int(st.secrets['MAX_THREADS']),
            'SCRAPE_DELAY': float(st.secrets['SCRAPE_DELAY']),
            'MIN_CONTENT_WORDS': int(st.secrets['MIN_CONTENT_WORDS']),
            'EXCLUDED_DOMAIN': st.secrets['EXCLUDED_DOMAIN'],
            'MISTRAL_API_KEY': st.secrets['MISTRAL_API_KEY'],
            'MISTRAL_MODEL': st.secrets['MISTRAL_MODEL'],
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
