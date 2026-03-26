from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """
    Interface base para provedores de LLM.
    Garante que qualquer provedor tenha o método ask.
    """
    @abstractmethod
    async def ask(self, prompt: str, system_prompt: str = None) -> str:
        raise NotImplementedError
