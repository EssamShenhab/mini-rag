from ..LLMInterface import LLMInterface
from openai import OpenAI
import logging
from typing import List, Union


class JinaProvider(LLMInterface):

    def __init__(
        self,
        api_key: str,
        api_url: str = "https://api.jina.ai/v1",
        default_input_max_characters: int = 1000,
    ):

        self.api_key = api_key
        self.api_url = api_url

        self.default_input_max_characters = default_input_max_characters

        self.generation_model_id = None  # Jina does not support generation
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_url,
        )

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        # Jina does not support LLM generation
        self.generation_model_id = model_id
        self.logger.warning("JinaProvider does not support text generation")

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def generate_text(
        self,
        prompt: str,
        chat_history: list = None,
        max_output_tokens: int = None,
        temperature: float = None,
    ):
        self.logger.error("JinaProvider does not support text generation")
        raise NotImplementedError("JinaProvider supports embeddings only")

    def embed_text(self, text: Union[str, List[str]], document_type: str = None):

        if not self.client:
            self.logger.error("Jina client was not initialized")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model for Jina was not set")
            return None

        if isinstance(text, str):
            text = [text]

        # Optional trimming
        text = [t[: self.default_input_max_characters].strip() for t in text]

        response = self.client.embeddings.create(
            model=self.embedding_model_id,
            input=text,
        )

        if not response or not response.data or len(response.data) == 0:
            self.logger.error("Error while embedding text with Jina")
            return None

        embeddings = [rec.embedding for rec in response.data]

        # Optional dimension validation
        if self.embedding_size and len(embeddings[0]) != self.embedding_size:
            self.logger.warning(
                f"Embedding dimension mismatch. Expected {self.embedding_size}, "
                f"got {len(embeddings[0])}"
            )

        return embeddings

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": prompt,
        }
