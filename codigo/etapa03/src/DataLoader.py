"""
Carregador de Dados da Etapa 1
Trabalho de Teoria dos Grafos - Etapa 3

Carrega os dados CSV gerados na Etapa 1 e constrói grafos para análise.
"""

import csv
import os
from typing import Dict, List, Set, Tuple
from .AdjacencyListGraph import AdjacencyListGraph

class DataLoader:
    """
    Classe para carregar dados da Etapa 1 e construir grafos.
    """
    
    def __init__(self, data_dir: str = "../etapa01/data"):
        """
        Inicializa o carregador de dados.
        
        Args:
            data_dir: Diretório com os arquivos CSV da Etapa 1
        """
        self.data_dir = data_dir
        self.user_to_id = {}
        self.id_to_user = {}
        self.next_id = 0
    
    def _get_user_id(self, username: str) -> int:
        """
        Obtém ID numérico para um usuário (cria se não existir).
        
        Args:
            username: Nome do usuário
            
        Returns:
            ID numérico do usuário
        """
        if username not in self.user_to_id:
            self.user_to_id[username] = self.next_id
            self.id_to_user[self.next_id] = username
            self.next_id += 1
        return self.user_to_id[username]
    
    def load_csv_data(self) -> Dict[str, List[Dict]]:
        """
        Carrega todos os arquivos CSV da Etapa 1.
        
        Returns:
            Dicionário com os dados carregados
        """
        data = {}
        
        # Arquivos esperados da Etapa 1
        csv_files = {
            'issues': 'issues_mmdetection.csv',
            'pull_requests': 'pull_requests_mmdetection.csv',
            'issue_comments': 'issue_comments_mmdetection.csv',
            'pr_comments': 'pr_comments_mmdetection.csv',
            'pr_reviews': 'pr_reviews_mmdetection.csv'
        }
        
        for key, filename in csv_files.items():
            filepath = os.path.join(self.data_dir, filename)
            data[key] = []
            
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        data[key] = list(reader)
                    print(f"✓ Carregado {filename}: {len(data[key])} registros")
                except Exception as e:
                    print(f"✗ Erro ao carregar {filename}: {e}")
            else:
                print(f"⚠ Arquivo não encontrado: {filepath}")
        
        return data
    
    def build_collaboration_graph(self, data: Dict[str, List[Dict]]) -> AdjacencyListGraph:
        """
        Constrói grafo de colaboração integrado a partir dos dados.
        
        Implementa o mesmo sistema de pesos da Etapa 1:
        - Comentários: peso 2
        - Issues comentadas: peso 3  
        - Reviews: peso 4
        - Merges: peso 5
        
        Args:
            data: Dados carregados dos CSVs
            
        Returns:
            Grafo de colaboração
        """
        # Primeira passada: mapeia todos os usuários únicos
        all_users = set()
        
        for issues in data.get('issues', []):
            if issues.get('author'):
                all_users.add(issues['author'])
            if issues.get('closed_by'):
                all_users.add(issues['closed_by'])
        
        for prs in data.get('pull_requests', []):
            if prs.get('author'):
                all_users.add(prs['author'])
            if prs.get('merged_by'):
                all_users.add(prs['merged_by'])
        
        for comment in data.get('issue_comments', []):
            if comment.get('author'):
                all_users.add(comment['author'])
        
        for comment in data.get('pr_comments', []):
            if comment.get('author'):
                all_users.add(comment['author'])
        
        for review in data.get('pr_reviews', []):
            if review.get('reviewer'):
                all_users.add(review['reviewer'])
        
        # Remove valores vazios
        all_users.discard('')
        all_users.discard(None)
        
        # Cria IDs para todos os usuários
        for user in sorted(all_users):
            self._get_user_id(user)
        
        print(f"📊 Total de usuários únicos: {len(all_users)}")
        
        # Cria grafo
        graph = AdjacencyListGraph(len(all_users))
        
        # Mapeia issues para seus autores
        issue_authors = {}
        for issue in data.get('issues', []):
            if issue.get('number') and issue.get('author'):
                issue_authors[issue['number']] = issue['author']
        
        # Mapeia PRs para seus autores  
        pr_authors = {}
        for pr in data.get('pull_requests', []):
            if pr.get('number') and pr.get('author'):
                pr_authors[pr['number']] = pr['author']
        
        # Dicionário para acumular pesos das arestas
        edge_weights = {}
        
        def add_edge_weight(from_user: str, to_user: str, weight: int):
            """Adiciona peso à aresta entre dois usuários."""
            if from_user and to_user and from_user != to_user:
                from_id = self._get_user_id(from_user)
                to_id = self._get_user_id(to_user)
                
                key = (from_id, to_id)
                edge_weights[key] = edge_weights.get(key, 0) + weight
        
        # 1. Comentários em issues (peso 2 + 3)
        for comment in data.get('issue_comments', []):
            comment_author = comment.get('author')
            issue_number = comment.get('issue_number')
            
            if comment_author and issue_number in issue_authors:
                issue_author = issue_authors[issue_number]
                add_edge_weight(comment_author, issue_author, 2)  # Comentário
                add_edge_weight(issue_author, comment_author, 3)  # Issue comentada
        
        # 2. Comentários em PRs (peso 2 + 3)
        for comment in data.get('pr_comments', []):
            comment_author = comment.get('author')
            pr_number = comment.get('pr_number')
            
            if comment_author and pr_number in pr_authors:
                pr_author = pr_authors[pr_number]
                add_edge_weight(comment_author, pr_author, 2)  # Comentário
                add_edge_weight(pr_author, comment_author, 3)  # PR comentado
        
        # 3. Reviews (peso 4)
        for review in data.get('pr_reviews', []):
            reviewer = review.get('reviewer')
            pr_number = review.get('pr_number')
            
            if reviewer and pr_number in pr_authors:
                pr_author = pr_authors[pr_number]
                add_edge_weight(reviewer, pr_author, 4)  # Review
        
        # 4. Fechamento de issues (peso 3)
        for issue in data.get('issues', []):
            issue_author = issue.get('author')
            closed_by = issue.get('closed_by')
            
            if issue_author and closed_by and issue_author != closed_by:
                add_edge_weight(closed_by, issue_author, 3)  # Fechamento
        
        # 5. Merges (peso 5)
        for pr in data.get('pull_requests', []):
            pr_author = pr.get('author')
            merged_by = pr.get('merged_by')
            
            if pr_author and merged_by and pr_author != merged_by:
                add_edge_weight(merged_by, pr_author, 5)  # Merge
        
        # Adiciona arestas ao grafo com pesos
        total_edges = 0
        for (from_id, to_id), weight in edge_weights.items():
            graph.addEdge(from_id, to_id)
            graph.setEdgeWeight(from_id, to_id, weight)
            total_edges += 1
        
        print(f"📊 Grafo construído:")
        print(f"   - Vértices: {graph.getVertexCount()}")
        print(f"   - Arestas: {graph.getEdgeCount()}")
        print(f"   - Peso total: {sum(edge_weights.values())}")
        
        return graph
    
    def get_user_mapping(self) -> Dict[int, str]:
        """
        Retorna mapeamento de IDs para nomes de usuários.
        
        Returns:
            Dicionário {id: username}
        """
        return self.id_to_user.copy()
    
    def get_top_users_by_degree(self, graph: AdjacencyListGraph, top_n: int = 20) -> List[Tuple[str, int]]:
        """
        Retorna os usuários com maior grau (mais conectados).
        
        Args:
            graph: Grafo de colaboração
            top_n: Número de usuários a retornar
            
        Returns:
            Lista de (username, grau_total) ordenada por grau
        """
        user_degrees = []
        
        for user_id in range(graph.getVertexCount()):
            username = self.id_to_user.get(user_id, f"user_{user_id}")
            total_degree = graph.getVertexInDegree(user_id) + graph.getVertexOutDegree(user_id)
            user_degrees.append((username, total_degree))
        
        # Ordena por grau (decrescente)
        user_degrees.sort(key=lambda x: x[1], reverse=True)
        
        return user_degrees[:top_n]