import os
from typing import Literal, Optional

from mem0.configs.embeddings.base import BaseEmbedderConfig
from mem0.embeddings.base import EmbeddingBase

try:
    from openai import OpenAI
except ImportError:
    raise ImportError("The 'openai' library is required for Mistral. Please install it using 'pip install openai'.")


class MistralEmbedding(EmbeddingBase):
    def __init__(self, config: Optional[BaseEmbedderConfig] = None):
        super().__init__(config)

        self.config.model = self.config.model or "mistral-embed"
        self.config.embedding_dims = self.config.embedding_dims or 1024

        api_key = self.config.api_key or os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("Mistral API key is required. Set MISTRAL_API_KEY environment variable or pass it in config.")

        # Use OpenAI client with Mistral API base URL
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.mistral.ai/v1"
        )

    def embed(self, text, memory_action: Optional[Literal["add", "search", "update"]] = None):
        """
        Get the embedding for the given text using Mistral API.

        Args:
            text (str): The text to embed.
            memory_action (optional): The type of embedding to use. Must be one of "add", "search", or "update". Defaults to None.
        
        Returns:
            list: The embedding vector.
        """
        response = self.client.embeddings.create(
            model=self.config.model,
            input=[text] if isinstance(text, str) else text,
            encoding_format="float"
        )
        
        # Return the first embedding if input was a string
        if isinstance(text, str):
            return response.data[0].embedding
        else:
            return [item.embedding for item in response.data] 