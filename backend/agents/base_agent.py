from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dotenv import load_dotenv
import os

load_dotenv()

from tools.llm_adapter import LLMAdapter


class BaseAgent(ABC):
    def __init__(self, name: str, model: str = "gpt-3.5-turbo"):
        self.name = name
        self.model = model
        # Use the LLM adapter which handles real vs mock LLM calls
        self.llm = LLMAdapter(model=self.model)

    @abstractmethod
    def process_request(self, request: str) -> str:
        """Process a request and return a response"""
        pass

    def _call_llm(self, messages: List[Dict[str, str]]) -> str:
        """Call the configured LLM adapter with the provided messages"""
        try:
            return self.llm.chat(messages)
        except Exception as e:
            return f"Error calling LLM adapter: {e}"