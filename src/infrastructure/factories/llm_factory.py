import os
from src.core.interfaces.llm_provider import LLMProvider
from src.infrastructure.providers.anthropic_provider import AnthropicProvider
from src.infrastructure.providers.gemini_provider import GeminiProvider

class LLMFactory:
    """
    Fábrica responsável por instanciar o provedor de LLM correto
    baseado na variável de ambiente AI_MODEL_TYPE.
    """
    @staticmethod
    def get_provider() -> LLMProvider:
        provider_type = os.getenv("AI_MODEL_TYPE", "anthropic").lower()
        
        if provider_type == "anthropic":
            return AnthropicProvider()
        elif provider_type == "gemini":
            return GeminiProvider()
        else:
            raise ValueError(f"Provedor de IA '{provider_type}' não suportado ou configurado incorretamente.")
