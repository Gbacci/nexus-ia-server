import os
from anthropic import AsyncAnthropic
from src.core.interfaces.llm_provider import LLMProvider

class AnthropicProvider(LLMProvider):
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY não está configurada. Verifique seu arquivo .env.")
        
        # Utilizamos AsyncAnthropic para suportar chamadas assíncronas no FastAPI
        self.client = AsyncAnthropic(api_key=api_key)

    async def ask(self, prompt: str, system_prompt: str = None) -> str:
        # Prepara os parâmetros da chamada
        kwargs = {
            "model": "claude-3-5-sonnet-latest",
            "max_tokens": 2048,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        # Injeta o System Prompt do RAG se existir
        if system_prompt:
            kwargs["system"] = system_prompt

        response = await self.client.messages.create(**kwargs)
        return response.content[0].text
