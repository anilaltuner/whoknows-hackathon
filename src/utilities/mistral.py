from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from config import config


class Mistral:
    def __init__(self):
        self.client = MistralClient(api_key=config.MISTRAL_API_KEY)
        self.model = config.MISTRAL_MODEL

    def chat(self, query):
        chat_response = self.client.chat_stream(
            model=self.model,
            messages=[ChatMessage(role='system', content="Output must be maximum 400 token."),
                      ChatMessage(role='user', content=query)],
        )
        for chunk in chat_response:
            if chunk.choices:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
