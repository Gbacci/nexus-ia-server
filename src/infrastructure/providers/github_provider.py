from typing import List, Dict
from github import Github
from src.core.interfaces.github_provider_interface import GitHubProviderInterface

class GitHubProvider(GitHubProviderInterface):
    """
    Provedor real de dados do GitHub utilizando a biblioteca PyGithub.
    Busca arquivos diretamente da API em memória, ignorando download e clonagem para o disco.
    """
    def __init__(self):
        self.target_extensions = ['.py', '.dart', '.ts', '.js']

    def list_repositories(self, access_token: str) -> List[Dict]:
        g = Github(access_token)
        repos = []
        # get_repos() retorna todos onde o user for owner ou collaborator
        for repo in g.get_user().get_repos():
            repos.append({
                'id': str(repo.id),
                'name': repo.full_name,
                'url': repo.clone_url
            })
        return repos

    def get_repository_content(self, access_token: str, repo_id: str) -> List[Dict]:
        g = Github(access_token)
        repo = g.get_repo(int(repo_id))
        
        extracted_files = []
        
        # Função recursiva para varrer a árvore via API
        def traverse_dir(path=""):
            contents = repo.get_contents(path)
            # contents pode ser uma lista (diretório) ou um objeto (arquivo único)
            if not isinstance(contents, list):
                contents = [contents]
                
            for content_file in contents:
                # Ignorar pastas padronizadas
                if any(ignored in content_file.path for ignored in ['node_modules', 'venv', '.git', '__pycache__', '.dart_tool']):
                    continue
                    
                if content_file.type == "dir":
                    traverse_dir(content_file.path)
                elif content_file.type == "file" and any(content_file.name.endswith(ext) for ext in self.target_extensions):
                    try:
                        file_content = content_file.decoded_content.decode('utf-8')
                        extracted_files.append({
                            'file_path': content_file.path,
                            'content': file_content
                        })
                    except Exception as e:
                        print(f"[-] Erro ao decodificar {content_file.path}: {e}")

        # Inicia a varredura pela raiz do projeto
        traverse_dir()
        return extracted_files
