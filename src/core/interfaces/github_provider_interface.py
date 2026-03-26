from abc import ABC, abstractmethod
from typing import List, Dict

class GitHubProviderInterface(ABC):
    """
    Interface para provedores de controle de versão (Ports and Adapters).
    Permite a listagem e extração de arquivos de repositórios do usuário.
    """
    
    @abstractmethod
    def list_repositories(self, access_token: str) -> List[Dict]:
        """
        Retorna uma lista de dicionários contendo ids e nomes de repositórios.
        Ex: [{'id': '12345', 'name': 'nexus_ai_server'}]
        """
        raise NotImplementedError

    @abstractmethod
    def get_repository_content(self, access_token: str, repo_id: str) -> List[Dict]:
        """
        Retorna os blocos de texto puros de todos os arquivos suportados no repositório.
        Ex: [{'file_path': 'src/main.py', 'content': 'import os\n...'}]
        """
        raise NotImplementedError
