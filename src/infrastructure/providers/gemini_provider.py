import os
import google.generativeai as genai
from src.core.interfaces.llm_provider import LLMProvider

class GeminiProvider(LLMProvider):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY não está configurada. Verifique seu arquivo .env.")
        
        # Configura a API do Google Generative AI
        genai.configure(api_key=api_key)
        # Inicializa o modelo solicitado (Gemini 1.5 Flash)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def ask(self, prompt: str, system_prompt: str = None) -> str:
        # Se houver System Prompt, recria-se o modelo momentaneamente ou usando kwargs assíncronos (gemini-1.5-pro suporta nativamente, flash tbm).
        if system_prompt:
            model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_prompt)
        else:
            model = self.model

        # Usa o método assíncrono para geração de conteúdo
        response = await model.generate_content_async(prompt)
        return response.text
