"""
Analisador de Grafos com Métricas Avançadas
Trabalho de Teoria dos Grafos - Etapa 3

Implementa TODOS os algoritmos de análise de grafos DO ZERO.
Sem usar bibliotecas prontas para análise de grafos.
Apenas estruturas básicas do Python.
"""

from typing import Dict, List, Tuple, Set
from .AbstractGraph import AbstractGraph

class GraphAnalyzer:
    """
    Classe para análise de grafos implementada completamente do zero.
    Todos os algoritmos são implementados manualmente.
    """
    
    def __init__(self, graph: AbstractGraph = None):
        """
        Inicializa o analisador.
        
        Args:
            graph: Grafo a ser analisado
        """
        self.graph = graph
        self.num_vertices = graph.getVertexCount() if graph else 0
    
    # =================================================================
    # ALGORITMOS DE BUSCA (BASE PARA OUTRAS MÉTRICAS)
    # =================================================================
    
    def _bfs_distances(self, start: int) -> Dict[int, int]:
        """
        Busca em largura para calcular distâncias.
        Implementado do zero usando lista como fila.
        
        Args:
            start: Vértice inicial
            
        Returns:
            Dicionário {vértice: distância}
        """
        distances = {start: 0}
        queue = [start]  # Fila simples com lista
        
        while queue:
            current = queue.pop(0)  # Remove do início (FIFO)
            
            # Pega sucessores do vértice atual
            successors = self.graph.getSuccessors(current)
            
            for neighbor in successors:
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        
        return distances
    
    # =================================================================
    # MÉTRICAS DE CENTRALIDADE - IMPLEMENTADAS DO ZERO
    # =================================================================
    
    def calculate_degree_centrality(self) -> Dict[int, float]:
        """
        Centralidade de grau implementada do zero.
        
        Returns:
            Dicionário {vértice: centralidade_grau}
        """
        centrality = {}
        max_possible_degree = self.num_vertices - 1
        
        for v in range(self.num_vertices):
            # Conta grau de entrada + saída
            in_degree = self.graph.getVertexInDegree(v)
            out_degree = self.graph.getVertexOutDegree(v)
            total_degree = in_degree + out_degree
            
            # Normaliza
            if max_possible_degree > 0:
                centrality[v] = total_degree / (2 * max_possible_degree)
            else:
                centrality[v] = 0.0
        
        return centrality
    
    def calculate_betweenness_centrality(self) -> Dict[int, float]:
        """
        Centralidade de intermediação implementada do zero.
        Algoritmo de Brandes simplificado.
        
        Returns:
            Dicionário {vértice: centralidade_intermediacao}
        """
        centrality = {v: 0.0 for v in range(self.num_vertices)}
        
        for s in range(self.num_vertices):
            # Inicialização
            stack = []
            predecessors = {v: [] for v in range(self.num_vertices)}
            distances = {v: -1 for v in range(self.num_vertices)}
            sigma = {v: 0 for v in range(self.num_vertices)}
            delta = {v: 0.0 for v in range(self.num_vertices)}
            
            # BFS modificada
            distances[s] = 0
            sigma[s] = 1
            queue = [s]
            
            while queue:
                v = queue.pop(0)
                stack.append(v)
                
                successors = self.graph.getSuccessors(v)
                for w in successors:
                    # Primeira vez encontrando w?
                    if distances[w] < 0:
                        queue.append(w)
                        distances[w] = distances[v] + 1
                    
                    # Caminho mínimo até w através de v?
                    if distances[w] == distances[v] + 1:
                        sigma[w] += sigma[v]
                        predecessors[w].append(v)
            
            # Acumulação
            while stack:
                w = stack.pop()
                for v in predecessors[w]:
                    delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
                if w != s:
                    centrality[w] += delta[w]
        
        # Normalização
        n = self.num_vertices
        norm_factor = 2.0 / ((n - 1) * (n - 2)) if n > 2 else 1.0
        
        for v in centrality:
            centrality[v] *= norm_factor
        
        return centrality
    
    def calculate_closeness_centrality(self) -> Dict[int, float]:
        """
        Centralidade de proximidade implementada do zero.
        
        Returns:
            Dicionário {vértice: centralidade_proximidade}
        """
        centrality = {}
        
        for v in range(self.num_vertices):
            distances = self._bfs_distances(v)
            
            # Remove vértices não alcançáveis
            reachable_distances = [d for d in distances.values() if d > 0]
            
            if len(reachable_distances) > 0:
                total_distance = sum(reachable_distances)
                # Closeness = (n-1) / soma_distancias
                centrality[v] = len(reachable_distances) / total_distance
            else:
                centrality[v] = 0.0
        
        return centrality
    
    def calculate_pagerank(self, damping: float = 0.85, max_iterations: int = 100, tolerance: float = 1e-6) -> Dict[int, float]:
        """
        PageRank implementado do zero.
        
        Args:
            damping: Fator de amortecimento
            max_iterations: Máximo de iterações
            tolerance: Tolerância para convergência
            
        Returns:
            Dicionário {vértice: pagerank}
        """
        # Inicialização
        pagerank = {v: 1.0 / self.num_vertices for v in range(self.num_vertices)}
        
        for iteration in range(max_iterations):
            new_pagerank = {}
            
            for v in range(self.num_vertices):
                rank_sum = 0.0
                
                # Soma contribuições dos predecessores
                for u in range(self.num_vertices):
                    if self.graph.hasEdge(u, v):
                        out_degree = self.graph.getVertexOutDegree(u)
                        if out_degree > 0:
                            rank_sum += pagerank[u] / out_degree
                
                # Fórmula do PageRank
                new_pagerank[v] = (1 - damping) / self.num_vertices + damping * rank_sum
            
            # Verifica convergência
            diff = sum(abs(new_pagerank[v] - pagerank[v]) for v in range(self.num_vertices))
            if diff < tolerance:
                break
            
            pagerank = new_pagerank
        
        return pagerank
    
    def calculate_eigenvector_centrality(self, max_iterations: int = 100, tolerance: float = 1e-6) -> Dict[int, float]:
        """
        Centralidade de autovetor implementada do zero.
        Método da potência.
        
        Args:
            max_iterations: Máximo de iterações
            tolerance: Tolerância para convergência
            
        Returns:
            Dicionário {vértice: centralidade_autovetor}
        """
        # Inicialização
        centrality = {v: 1.0 for v in range(self.num_vertices)}
        
        for iteration in range(max_iterations):
            new_centrality = {v: 0.0 for v in range(self.num_vertices)}
            
            # Multiplica matriz de adjacência pelo vetor
            for v in range(self.num_vertices):
                for u in range(self.num_vertices):
                    if self.graph.hasEdge(u, v):
                        new_centrality[v] += centrality[u]
            
            # Normalização (raiz quadrada implementada manualmente)
            values = list(new_centrality.values())
            norm = (sum(x**2 for x in values)) ** 0.5  # Norma euclidiana
            
            if norm > 0:
                for v in new_centrality:
                    new_centrality[v] /= norm
            
            # Verifica convergência
            diff = sum(abs(new_centrality[v] - centrality[v]) for v in range(self.num_vertices))
            if diff < tolerance:
                break
            
            centrality = new_centrality
        
        return centrality
    
    # =================================================================
    # MÉTRICAS DE REDE - IMPLEMENTADAS DO ZERO
    # =================================================================
    
    def calculate_network_density(self) -> float:
        """
        Densidade da rede implementada do zero.
        
        Returns:
            Densidade (0 a 1)
        """
        if self.num_vertices <= 1:
            return 0.0
        
        max_possible_edges = self.num_vertices * (self.num_vertices - 1)
        actual_edges = self.graph.getEdgeCount()
        
        return actual_edges / max_possible_edges
    
    def calculate_average_clustering_coefficient(self) -> float:
        """
        Coeficiente de clustering médio implementado do zero.
        
        Returns:
            Clustering médio (0 a 1)
        """
        total_clustering = 0.0
        valid_vertices = 0
        
        for v in range(self.num_vertices):
            neighbors = list(self.graph.getSuccessors(v))
            degree = len(neighbors)
            
            if degree < 2:
                continue  # Não pode formar triângulos
            
            # Conta triângulos
            triangles = 0
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    if self.graph.hasEdge(neighbors[i], neighbors[j]):
                        triangles += 1
            
            # Clustering local
            max_triangles = degree * (degree - 1) / 2
            local_clustering = triangles / max_triangles if max_triangles > 0 else 0
            
            total_clustering += local_clustering
            valid_vertices += 1
        
        return total_clustering / valid_vertices if valid_vertices > 0 else 0.0
    
    def calculate_assortativity(self) -> float:
        """
        Coeficiente de assortatividade implementado do zero.
        Correlação de graus entre vértices conectados.
        
        Returns:
            Assortatividade (-1 a 1)
        """
        edges_data = []
        
        # Coleta dados das arestas
        for u in range(self.num_vertices):
            u_degree = self.graph.getVertexOutDegree(u) + self.graph.getVertexInDegree(u)
            successors = self.graph.getSuccessors(u)
            
            for v in successors:
                v_degree = self.graph.getVertexOutDegree(v) + self.graph.getVertexInDegree(v)
                edges_data.append((u_degree, v_degree))
        
        if len(edges_data) == 0:
            return 0.0
        
        # Calcula correlação de Pearson manualmente (sem bibliotecas)
        n = len(edges_data)
        sum_xy = sum(x * y for x, y in edges_data)
        sum_x = sum(x for x, y in edges_data)
        sum_y = sum(y for x, y in edges_data)
        sum_x2 = sum(x * x for x, y in edges_data)
        sum_y2 = sum(y * y for x, y in edges_data)
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator_x = (n * sum_x2 - sum_x * sum_x) ** 0.5
        denominator_y = (n * sum_y2 - sum_y * sum_y) ** 0.5
        denominator = denominator_x * denominator_y
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    # =================================================================
    # MÉTRICAS DE COMUNIDADE - IMPLEMENTADAS DO ZERO
    # =================================================================
    
    def calculate_modularity_simple(self) -> float:
        """
        Modularidade simples baseada na estrutura do grafo.
        Implementada do zero.
        
        Returns:
            Modularidade estimada
        """
        # Detecta comunidades simples baseado em conectividade
        communities = self._detect_simple_communities()
        
        if len(communities) <= 1:
            return 0.0
        
        total_edges = self.graph.getEdgeCount()
        if total_edges == 0:
            return 0.0
        
        modularity = 0.0
        
        for community in communities.values():
            # Arestas internas da comunidade
            internal_edges = 0
            total_degree = 0
            
            for v in community:
                successors = self.graph.getSuccessors(v)
                total_degree += len(successors)
                
                for neighbor in successors:
                    if neighbor in community:
                        internal_edges += 1
            
            # Modularidade da comunidade
            if total_edges > 0:
                expected = (total_degree / (2 * total_edges)) ** 2
                actual = internal_edges / total_edges
                modularity += actual - expected
        
        return modularity
    
    def _detect_simple_communities(self) -> Dict[int, Set[int]]:
        """
        Detecção simples de comunidades baseada em componentes conectadas.
        Implementada do zero usando BFS.
        
        Returns:
            Dicionário {community_id: {vertices}}
        """
        visited = set()
        communities = {}
        community_id = 0
        
        for start in range(self.num_vertices):
            if start not in visited:
                # BFS para encontrar componente conectada
                community = set()
                queue = [start]
                
                while queue:
                    v = queue.pop(0)
                    if v not in visited:
                        visited.add(v)
                        community.add(v)
                        
                        # Adiciona vizinhos (entrada + saída)
                        successors = self.graph.getSuccessors(v)
                        for neighbor in successors:
                            if neighbor not in visited:
                                queue.append(neighbor)
                        
                        # Predecessores (grafo direcionado)
                        for u in range(self.num_vertices):
                            if self.graph.hasEdge(u, v) and u not in visited:
                                queue.append(u)
                
                if len(community) > 0:
                    communities[community_id] = community
                    community_id += 1
        
        return communities
    
    def calculate_bridging_ties_ratio(self) -> float:
        """
        Proporção de ligações entre grupos.
        Implementada do zero.
        
        Returns:
            Proporção de arestas entre comunidades
        """
        communities = self._detect_simple_communities()
        
        if len(communities) <= 1:
            return 0.0
        
        # Mapeamento vértice -> comunidade
        vertex_to_community = {}
        for comm_id, vertices in communities.items():
            for v in vertices:
                vertex_to_community[v] = comm_id
        
        total_edges = 0
        bridging_edges = 0
        
        for u in range(self.num_vertices):
            successors = self.graph.getSuccessors(u)
            for v in successors:
                total_edges += 1
                
                # É uma ligação entre comunidades?
                if vertex_to_community.get(u, -1) != vertex_to_community.get(v, -1):
                    bridging_edges += 1
        
        return bridging_edges / total_edges if total_edges > 0 else 0.0