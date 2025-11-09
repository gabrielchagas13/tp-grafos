"""
Graph Models
Classes para modelagem de grafos de colaboração
"""

import networkx as nx
import pandas as pd
from typing import Dict, List, Tuple, Set
from collections import defaultdict
import json

class CollaborationNode:
    """Representa um nó (usuário) no grafo de colaboração"""
    
    def __init__(self, username: str):
        self.username = username
        self.metrics = {
            "total_interactions": 0,
            "comments_made": 0,
            "issues_closed": 0,
            "reviews_given": 0,
            "prs_merged": 0,
            "centrality_score": 0.0
        }
    
    def add_interaction(self, interaction_type: str, weight: int = 1):
        """Adiciona uma interação ao nó"""
        self.metrics["total_interactions"] += weight
        if interaction_type == "comment":
            self.metrics["comments_made"] += 1
        elif interaction_type == "issue_close":
            self.metrics["issues_closed"] += 1
        elif interaction_type == "review":
            self.metrics["reviews_given"] += 1
        elif interaction_type == "merge":
            self.metrics["prs_merged"] += 1
    
    def to_dict(self) -> Dict:
        """Converte o nó para dicionário"""
        return {
            "username": self.username,
            **self.metrics
        }

class CollaborationEdge:
    """Representa uma aresta (interação) no grafo de colaboração"""
    
    def __init__(self, source: str, target: str, interaction_type: str, weight: int = 1):
        self.source = source
        self.target = target
        self.interaction_type = interaction_type
        self.weight = weight
        self.count = 1
        self.interactions = [interaction_type]
    
    def add_interaction(self, interaction_type: str, weight: int = 1):
        """Adiciona uma nova interação à aresta"""
        self.weight += weight
        self.count += 1
        self.interactions.append(interaction_type)
    
    def to_dict(self) -> Dict:
        """Converte a aresta para dicionário"""
        return {
            "source": self.source,
            "target": self.target,
            "weight": self.weight,
            "count": self.count,
            "types": list(set(self.interactions))
        }

class CollaborationGraph:
    """Classe base para grafos de colaboração direcionados"""
    
    def __init__(self, name: str):
        self.name = name
        self.graph = nx.DiGraph()
        self.nodes = {}  # username -> CollaborationNode
        self.edges = {}  # (source, target) -> CollaborationEdge
        
    def add_node(self, username: str) -> CollaborationNode:
        """Adiciona um nó ao grafo"""
        if username not in self.nodes:
            self.nodes[username] = CollaborationNode(username)
            self.graph.add_node(username)
        return self.nodes[username]
    
    def add_edge(self, source: str, target: str, interaction_type: str, weight: int = 1):
        """Adiciona uma aresta ao grafo"""
        # Adiciona nós se não existirem
        self.add_node(source)
        self.add_node(target)
        
        # Atualiza métricas dos nós
        self.nodes[source].add_interaction(interaction_type, weight)
        
        # Adiciona ou atualiza aresta
        edge_key = (source, target)
        if edge_key in self.edges:
            self.edges[edge_key].add_interaction(interaction_type, weight)
        else:
            self.edges[edge_key] = CollaborationEdge(source, target, interaction_type, weight)
        
        # Atualiza grafo NetworkX
        if self.graph.has_edge(source, target):
            self.graph[source][target]['weight'] += weight
            self.graph[source][target]['count'] += 1
        else:
            self.graph.add_edge(source, target, weight=weight, count=1, type=interaction_type)
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas básicas do grafo"""
        return {
            "name": self.name,
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "total_weight": sum(edge.weight for edge in self.edges.values()),
            "density": nx.density(self.graph),
            "is_connected": nx.is_weakly_connected(self.graph)
        }
    
    def calculate_centrality_metrics(self):
        """Calcula métricas de centralidade para todos os nós"""
        if len(self.graph.nodes()) == 0:
            return
        
        # Centralidade de grau
        in_degree_centrality = nx.in_degree_centrality(self.graph)
        out_degree_centrality = nx.out_degree_centrality(self.graph)
        
        # Centralidade de proximidade
        try:
            closeness_centrality = nx.closeness_centrality(self.graph)
        except:
            closeness_centrality = {node: 0 for node in self.graph.nodes()}
        
        # Centralidade de intermediação
        try:
            betweenness_centrality = nx.betweenness_centrality(self.graph)
        except:
            betweenness_centrality = {node: 0 for node in self.graph.nodes()}
        
        # PageRank
        try:
            pagerank = nx.pagerank(self.graph)
        except:
            pagerank = {node: 0 for node in self.graph.nodes()}
        
        # Atualiza nós com métricas
        for username, node in self.nodes.items():
            node.metrics.update({
                "in_degree_centrality": in_degree_centrality.get(username, 0),
                "out_degree_centrality": out_degree_centrality.get(username, 0),
                "closeness_centrality": closeness_centrality.get(username, 0),
                "betweenness_centrality": betweenness_centrality.get(username, 0),
                "pagerank": pagerank.get(username, 0),
                "centrality_score": (
                    in_degree_centrality.get(username, 0) + 
                    out_degree_centrality.get(username, 0) + 
                    closeness_centrality.get(username, 0) + 
                    betweenness_centrality.get(username, 0) + 
                    pagerank.get(username, 0)
                ) / 5
            })
    
    def export_to_json(self, filepath: str):
        """Exporta o grafo para JSON"""
        data = {
            "name": self.name,
            "stats": self.get_stats(),
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "edges": [edge.to_dict() for edge in self.edges.values()]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def export_to_gexf(self, filepath: str):
        """Exporta o grafo para formato GEXF (Gephi)"""
        # Adiciona atributos dos nós ao grafo NetworkX
        for username, node in self.nodes.items():
            for key, value in node.metrics.items():
                self.graph.nodes[username][key] = value
        
        nx.write_gexf(self.graph, filepath)

class CommentGraph(CollaborationGraph):
    """Grafo de comentários em issues e pull requests"""
    
    def __init__(self):
        super().__init__("Comentários")
    
    def build_from_data(self, issues_df: pd.DataFrame, prs_df: pd.DataFrame, 
                       issue_comments_df: pd.DataFrame, pr_comments_df: pd.DataFrame):
        """Constrói o grafo a partir dos dados extraídos"""
        print("Construindo grafo de comentários...")
        
        # Comentários em issues
        for _, comment in issue_comments_df.iterrows():
            # Encontra o autor da issue
            issue_author = issues_df[issues_df['number'] == comment['issue_number']]['author'].iloc[0]
            comment_author = comment['author']
            
            if issue_author != comment_author:  # Não conta auto-comentários
                self.add_edge(comment_author, issue_author, "comment", 2)
        
        # Comentários em PRs
        for _, comment in pr_comments_df.iterrows():
            # Encontra o autor do PR
            pr_author = prs_df[prs_df['number'] == comment['pr_number']]['author'].iloc[0]
            comment_author = comment['author']
            
            if pr_author != comment_author:  # Não conta auto-comentários
                self.add_edge(comment_author, pr_author, "comment", 2)
        
        self.calculate_centrality_metrics()

class IssueCloseGraph(CollaborationGraph):
    """Grafo de fechamento de issues"""
    
    def __init__(self):
        super().__init__("Fechamento de Issues")
    
    def build_from_data(self, issues_df: pd.DataFrame):
        """Constrói o grafo a partir dos dados de issues"""
        print("Construindo grafo de fechamento de issues...")
        
        # Issues fechadas por outros usuários
        closed_issues = issues_df[(issues_df['state'] == 'closed') & 
                                 (issues_df['closed_by'].notna()) & 
                                 (issues_df['author'] != issues_df['closed_by'])]
        
        for _, issue in closed_issues.iterrows():
            author = issue['author']
            closer = issue['closed_by']
            
            # Aresta do closer para o author (quem fechou -> quem abriu)
            self.add_edge(closer, author, "issue_close", 3)
        
        self.calculate_centrality_metrics()

class ReviewGraph(CollaborationGraph):
    """Grafo de reviews, aprovações e merges de pull requests"""
    
    def __init__(self):
        super().__init__("Reviews e Merges")
    
    def build_from_data(self, prs_df: pd.DataFrame, pr_reviews_df: pd.DataFrame):
        """Constrói o grafo a partir dos dados de PRs e reviews"""
        print("Construindo grafo de reviews e merges...")
        
        # Reviews de PRs
        for _, review in pr_reviews_df.iterrows():
            # Encontra o autor do PR
            pr_author = prs_df[prs_df['number'] == review['pr_number']]['author'].iloc[0]
            reviewer = review['reviewer']
            
            if pr_author != reviewer:  # Não conta auto-reviews
                # Peso baseado no tipo de review
                weight = 4  # Review padrão
                if review['state'] == 'APPROVED':
                    weight = 4
                elif review['state'] == 'CHANGES_REQUESTED':
                    weight = 4
                
                self.add_edge(reviewer, pr_author, "review", weight)
        
        # Merges de PRs
        merged_prs = prs_df[(prs_df['state'] == 'closed') & 
                           (prs_df['merged_at'].notna()) & 
                           (prs_df['merged_by'].notna()) & 
                           (prs_df['author'] != prs_df['merged_by'])]
        
        for _, pr in merged_prs.iterrows():
            author = pr['author']
            merger = pr['merged_by']
            
            # Aresta do merger para o author (quem fez merge -> quem criou PR)
            self.add_edge(merger, author, "merge", 5)
        
        self.calculate_centrality_metrics()

class IntegratedGraph(CollaborationGraph):
    """Grafo integrado com todos os tipos de interação"""
    
    def __init__(self):
        super().__init__("Grafo Integrado")
        self.interaction_weights = {
            "comment": 2,
            "issue_comment": 3,  # Comentário em issue que o usuário abriu
            "review": 4,
            "merge": 5,
            "issue_close": 3
        }
    
    def build_from_data(self, issues_df: pd.DataFrame, prs_df: pd.DataFrame, 
                       issue_comments_df: pd.DataFrame, pr_comments_df: pd.DataFrame,
                       pr_reviews_df: pd.DataFrame):
        """Constrói o grafo integrado a partir de todos os dados"""
        print("Construindo grafo integrado...")
        
        # 1. Comentários em issues
        for _, comment in issue_comments_df.iterrows():
            issue_author = issues_df[issues_df['number'] == comment['issue_number']]['author'].iloc[0]
            comment_author = comment['author']
            
            if issue_author != comment_author:
                self.add_edge(comment_author, issue_author, "issue_comment", 
                            self.interaction_weights["issue_comment"])
        
        # 2. Comentários em PRs
        for _, comment in pr_comments_df.iterrows():
            pr_author = prs_df[prs_df['number'] == comment['pr_number']]['author'].iloc[0]
            comment_author = comment['author']
            
            if pr_author != comment_author:
                self.add_edge(comment_author, pr_author, "comment", 
                            self.interaction_weights["comment"])
        
        # 3. Fechamento de issues
        closed_issues = issues_df[(issues_df['state'] == 'closed') & 
                                 (issues_df['closed_by'].notna()) & 
                                 (issues_df['author'] != issues_df['closed_by'])]
        
        for _, issue in closed_issues.iterrows():
            author = issue['author']
            closer = issue['closed_by']
            self.add_edge(closer, author, "issue_close", 
                         self.interaction_weights["issue_close"])
        
        # 4. Reviews de PRs
        for _, review in pr_reviews_df.iterrows():
            pr_author = prs_df[prs_df['number'] == review['pr_number']]['author'].iloc[0]
            reviewer = review['reviewer']
            
            if pr_author != reviewer:
                self.add_edge(reviewer, pr_author, "review", 
                            self.interaction_weights["review"])
        
        # 5. Merges de PRs
        merged_prs = prs_df[(prs_df['state'] == 'closed') & 
                           (prs_df['merged_at'].notna()) & 
                           (prs_df['merged_by'].notna()) & 
                           (prs_df['author'] != prs_df['merged_by'])]
        
        for _, pr in merged_prs.iterrows():
            author = pr['author']
            merger = pr['merged_by']
            self.add_edge(merger, author, "merge", 
                         self.interaction_weights["merge"])
        
        self.calculate_centrality_metrics()
    
    def get_top_collaborators(self, n: int = 10) -> List[Dict]:
        """Retorna os top N colaboradores por score de centralidade"""
        sorted_nodes = sorted(
            self.nodes.values(), 
            key=lambda x: x.metrics["centrality_score"], 
            reverse=True
        )
        
        return [node.to_dict() for node in sorted_nodes[:n]]
    
    def get_interaction_summary(self) -> Dict:
        """Retorna resumo das interações por tipo"""
        summary = defaultdict(int)
        
        for edge in self.edges.values():
            for interaction in edge.interactions:
                summary[interaction] += 1
        
        return dict(summary)