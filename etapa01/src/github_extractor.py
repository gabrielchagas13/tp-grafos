"""
GitHub Data Extractor
Módulo para extração de dados de issues, pull requests e interações do GitHub
"""

import requests
import json
import time
import os
from datetime import datetime
from typing import List, Dict, Optional
from tqdm import tqdm
import pandas as pd
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class GitHubDataExtractor:
    def __init__(self, repo_owner: str, repo_name: str, token: Optional[str] = None):
        """
        Inicializa o extrator de dados do GitHub
        
        Args:
            repo_owner: Proprietário do repositório
            repo_name: Nome do repositório
            token: Token de acesso do GitHub (opcional)
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        
        # Headers para requisições
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Graph-Analysis"
        }
        
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
    
    def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """
        Faz uma requisição para a API do GitHub com tratamento de rate limit
        
        Args:
            url: URL da API
            params: Parâmetros da requisição
            
        Returns:
            Resposta da API ou None em caso de erro
        """
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            # Verifica rate limit
            if response.status_code == 403 and 'rate limit' in response.text.lower():
                reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                wait_time = max(0, reset_time - int(time.time()) + 1)
                print(f"Rate limit atingido. Aguardando {wait_time} segundos...")
                time.sleep(wait_time)
                return self._make_request(url, params)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return None
    
    def _paginate_request(self, url: str, params: Dict = None, max_items: int = None) -> List[Dict]:
        """
        Faz requisições paginadas para a API do GitHub
        
        Args:
            url: URL da API
            params: Parâmetros da requisição
            max_items: Número máximo de itens para retornar
            
        Returns:
            Lista com todos os itens das páginas
        """
        items = []
        page = 1
        params = params or {}
        
        with tqdm(desc="Coletando dados") as pbar:
            while True:
                params.update({"page": page, "per_page": 100})
                data = self._make_request(url, params)
                
                if not data or len(data) == 0:
                    break
                
                items.extend(data)
                pbar.update(len(data))
                
                if max_items and len(items) >= max_items:
                    items = items[:max_items]
                    break
                
                page += 1
                time.sleep(0.1)  # Pequena pausa entre requisições
        
        return items
    
    def extract_issues(self, max_issues: int = 1000) -> pd.DataFrame:
        """
        Extrai dados de issues do repositório
        
        Args:
            max_issues: Número máximo de issues para extrair
            
        Returns:
            DataFrame com dados das issues
        """
        print(f"Extraindo issues do repositório {self.repo_owner}/{self.repo_name}...")
        
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues"
        params = {"state": "all", "sort": "updated", "direction": "desc"}
        
        issues = self._paginate_request(url, params, max_issues)
        
        # Processa dados das issues
        processed_issues = []
        for issue in issues:
            processed_issues.append({
                "id": issue.get("id", 0),
                "number": issue.get("number", 0),
                "title": issue.get("title", ""),
                "state": issue.get("state", "unknown"),
                "author": issue.get("user", {}).get("login", "unknown"),
                "created_at": issue.get("created_at", ""),
                "updated_at": issue.get("updated_at", ""),
                "closed_at": issue.get("closed_at"),
                "closed_by": issue.get("closed_by", {}).get("login") if issue.get("closed_by") else None,
                "comments_count": issue.get("comments", 0),
                "is_pull_request": "pull_request" in issue
            })
        
        df = pd.DataFrame(processed_issues)
        df.to_csv(f"data/issues_{self.repo_name}.csv", index=False)
        print(f"Extraídas {len(df)} issues")
        
        return df
    
    def extract_pull_requests(self, max_prs: int = 1000) -> pd.DataFrame:
        """
        Extrai dados de pull requests do repositório
        
        Args:
            max_prs: Número máximo de PRs para extrair
            
        Returns:
            DataFrame com dados dos PRs
        """
        print(f"Extraindo pull requests do repositório {self.repo_owner}/{self.repo_name}...")
        
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/pulls"
        params = {"state": "all", "sort": "updated", "direction": "desc"}
        
        prs = self._paginate_request(url, params, max_prs)
        
        # Processa dados dos PRs
        processed_prs = []
        for pr in prs:
            processed_prs.append({
                "id": pr.get("id", 0),
                "number": pr.get("number", 0),
                "title": pr.get("title", ""),
                "state": pr.get("state", "unknown"),
                "author": pr.get("user", {}).get("login", "unknown"),
                "created_at": pr.get("created_at", ""),
                "updated_at": pr.get("updated_at", ""),
                "closed_at": pr.get("closed_at"),
                "merged_at": pr.get("merged_at"),
                "merged_by": pr.get("merged_by", {}).get("login") if pr.get("merged_by") else None,
                "comments_count": pr.get("comments", 0),
                "review_comments_count": pr.get("review_comments", 0),
                "commits_count": pr.get("commits", 0),
                "additions": pr.get("additions", 0),
                "deletions": pr.get("deletions", 0)
            })
        
        df = pd.DataFrame(processed_prs)
        df.to_csv(f"data/pull_requests_{self.repo_name}.csv", index=False)
        print(f"Extraídos {len(df)} pull requests")
        
        return df
    
    def extract_issue_comments(self, issue_numbers: List[int]) -> pd.DataFrame:
        """
        Extrai comentários de issues específicas
        
        Args:
            issue_numbers: Lista de números das issues
            
        Returns:
            DataFrame com comentários das issues
        """
        print("Extraindo comentários das issues...")
        
        all_comments = []
        
        for issue_number in tqdm(issue_numbers, desc="Issues"):
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}/comments"
            comments = self._paginate_request(url)
            
            for comment in comments:
                all_comments.append({
                    "id": comment["id"],
                    "issue_number": issue_number,
                    "author": comment["user"]["login"],
                    "created_at": comment["created_at"],
                    "updated_at": comment["updated_at"],
                    "body_length": len(comment["body"])
                })
            
            time.sleep(0.1)  # Pausa entre requisições
        
        df = pd.DataFrame(all_comments)
        df.to_csv(f"data/issue_comments_{self.repo_name}.csv", index=False)
        print(f"Extraídos {len(df)} comentários de issues")
        
        return df
    
    def extract_pr_reviews(self, pr_numbers: List[int]) -> pd.DataFrame:
        """
        Extrai reviews de pull requests específicos
        
        Args:
            pr_numbers: Lista de números dos PRs
            
        Returns:
            DataFrame com reviews dos PRs
        """
        print("Extraindo reviews dos pull requests...")
        
        all_reviews = []
        
        for pr_number in tqdm(pr_numbers, desc="PRs"):
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/pulls/{pr_number}/reviews"
            reviews = self._paginate_request(url)
            
            for review in reviews:
                all_reviews.append({
                    "id": review["id"],
                    "pr_number": pr_number,
                    "reviewer": review["user"]["login"],
                    "state": review["state"],  # APPROVED, CHANGES_REQUESTED, COMMENTED
                    "submitted_at": review["submitted_at"],
                    "body_length": len(review["body"]) if review["body"] else 0
                })
            
            time.sleep(0.1)  # Pausa entre requisições
        
        df = pd.DataFrame(all_reviews)
        df.to_csv(f"data/pr_reviews_{self.repo_name}.csv", index=False)
        print(f"Extraídos {len(df)} reviews de PRs")
        
        return df
    
    def extract_pr_comments(self, pr_numbers: List[int]) -> pd.DataFrame:
        """
        Extrai comentários de pull requests específicos
        
        Args:
            pr_numbers: Lista de números dos PRs
            
        Returns:
            DataFrame com comentários dos PRs
        """
        print("Extraindo comentários dos pull requests...")
        
        all_comments = []
        
        for pr_number in tqdm(pr_numbers, desc="PRs"):
            # Comentários gerais do PR
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues/{pr_number}/comments"
            comments = self._paginate_request(url)
            
            for comment in comments:
                all_comments.append({
                    "id": comment["id"],
                    "pr_number": pr_number,
                    "author": comment["user"]["login"],
                    "created_at": comment["created_at"],
                    "type": "issue_comment",
                    "body_length": len(comment["body"])
                })
            
            # Comentários de review
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/pulls/{pr_number}/comments"
            review_comments = self._paginate_request(url)
            
            for comment in review_comments:
                all_comments.append({
                    "id": comment["id"],
                    "pr_number": pr_number,
                    "author": comment["user"]["login"],
                    "created_at": comment["created_at"],
                    "type": "review_comment",
                    "body_length": len(comment["body"])
                })
            
            time.sleep(0.1)  # Pausa entre requisições
        
        df = pd.DataFrame(all_comments)
        df.to_csv(f"data/pr_comments_{self.repo_name}.csv", index=False)
        print(f"Extraídos {len(df)} comentários de PRs")
        
        return df
    
    def extract_all_data(self, max_issues: int = 1000, max_prs: int = 1000) -> Dict[str, pd.DataFrame]:
        """
        Extrai todos os dados necessários do repositório
        
        Args:
            max_issues: Número máximo de issues
            max_prs: Número máximo de PRs
            
        Returns:
            Dicionário com todos os DataFrames extraídos
        """
        print(f"Iniciando extração completa do repositório {self.repo_owner}/{self.repo_name}")
        
        # Extrai issues e PRs
        issues_df = self.extract_issues(max_issues)
        prs_df = self.extract_pull_requests(max_prs)
        
        # Filtra apenas issues (não PRs)
        real_issues_df = issues_df[~issues_df['is_pull_request']].copy()
        
        # Extrai comentários e reviews
        issue_numbers = real_issues_df['number'].tolist()[:100]  # Limita para evitar muitas requisições
        pr_numbers = prs_df['number'].tolist()[:100]  # Limita para evitar muitas requisições
        
        issue_comments_df = self.extract_issue_comments(issue_numbers)
        pr_reviews_df = self.extract_pr_reviews(pr_numbers)
        pr_comments_df = self.extract_pr_comments(pr_numbers)
        
        return {
            "issues": real_issues_df,
            "pull_requests": prs_df,
            "issue_comments": issue_comments_df,
            "pr_reviews": pr_reviews_df,
            "pr_comments": pr_comments_df
        }

if __name__ == "__main__":
    # Configuração
    REPO_OWNER = os.getenv('REPO_OWNER', 'open-mmlab')
    REPO_NAME = os.getenv('REPO_NAME', 'mmdetection')
    MAX_ISSUES = int(os.getenv('MAX_ISSUES', 500))
    MAX_PRS = int(os.getenv('MAX_PRS', 500))
    
    # Inicializa extrator
    extractor = GitHubDataExtractor(REPO_OWNER, REPO_NAME)
    
    # Extrai todos os dados
    data = extractor.extract_all_data(MAX_ISSUES, MAX_PRS)
    
    print("\nExtração concluída!")
    print("Arquivos salvos na pasta 'data/':")
    for key, df in data.items():
        print(f"  - {key}: {len(df)} registros")