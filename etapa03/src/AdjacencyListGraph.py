"""
Classe AdjacencyListGraph
Trabalho de Teoria dos Grafos - Etapa 2/3

Implementação da API utilizando listas de adjacência.
"""

from typing import Dict, List, Set
from .AbstractGraph import AbstractGraph

class AdjacencyListGraph(AbstractGraph):
    """
    Implementação de grafo usando listas de adjacência.
    
    Cada vértice mantém um conjunto (set) de seus sucessores.
    """
    
    def __init__(self, num_vertices: int):
        """
        Inicializa grafo com listas de adjacência.
        
        Args:
            num_vertices: Número de vértices do grafo
            
        Raises:
            ValueError: Se num_vertices <= 0
        """
        super().__init__(num_vertices)
        
        # Inicializa listas de adjacência
        self._adj_list: Dict[int, Set[int]] = {
            i: set() for i in range(num_vertices)
        }
    
    def getVertexCount(self) -> int:
        """Retorna o número de vértices do grafo."""
        return self._num_vertices
    
    def getEdgeCount(self) -> int:
        """Retorna o número de arestas do grafo."""
        edge_count = 0
        for vertex in self._adj_list:
            edge_count += len(self._adj_list[vertex])
        return edge_count
    
    def hasEdge(self, u: int, v: int) -> bool:
        """Verifica se existe aresta entre u e v."""
        self._validate_vertices(u, v)
        return v in self._adj_list[u]
    
    def addEdge(self, u: int, v: int) -> None:
        """Adiciona aresta entre u e v (operação idempotente)."""
        self._validate_vertices(u, v)
        self._validate_no_self_loop(u, v)
        self._adj_list[u].add(v)
    
    def removeEdge(self, u: int, v: int) -> None:
        """Remove aresta entre u e v."""
        self._validate_vertices(u, v)
        self._adj_list[u].discard(v)
        if (u, v) in self._edge_weights:
            del self._edge_weights[(u, v)]
    
    def isSucessor(self, u: int, v: int) -> bool:
        """Verifica se v é sucessor de u."""
        return self.hasEdge(u, v)
    
    def isPredessor(self, u: int, v: int) -> bool:
        """Verifica se u é predecessor de v."""
        return self.hasEdge(u, v)
    
    def getVertexInDegree(self, u: int) -> int:
        """Retorna o grau de entrada do vértice u."""
        self._validate_vertex(u)
        in_degree = 0
        for vertex in self._adj_list:
            if u in self._adj_list[vertex]:
                in_degree += 1
        return in_degree
    
    def getVertexOutDegree(self, u: int) -> int:
        """Retorna o grau de saída do vértice u."""
        self._validate_vertex(u)
        return len(self._adj_list[u])
    
    def isConnected(self) -> bool:
        """Verifica se o grafo é conectado usando DFS."""
        if self._num_vertices <= 1:
            return True
        visited = [False] * self._num_vertices
        self._dfs_connected(0, visited)
        return all(visited)
    
    def _dfs_connected(self, vertex: int, visited: List[bool]) -> None:
        """DFS auxiliar para verificação de conectividade."""
        visited[vertex] = True
        for successor in self._adj_list[vertex]:
            if not visited[successor]:
                self._dfs_connected(successor, visited)
        for v in range(self._num_vertices):
            if not visited[v] and vertex in self._adj_list[v]:
                self._dfs_connected(v, visited)
    
    def getSuccessors(self, u: int) -> Set[int]:
        """Retorna os sucessores do vértice u."""
        self._validate_vertex(u)
        return self._adj_list[u].copy()
    
    def getPredecessors(self, u: int) -> Set[int]:
        """Retorna os predecessores do vértice u."""
        self._validate_vertex(u)
        predecessors = set()
        for vertex in self._adj_list:
            if u in self._adj_list[vertex]:
                predecessors.add(vertex)
        return predecessors
    
    def getAdjacencyList(self) -> Dict[int, Set[int]]:
        """Retorna cópia das listas de adjacência."""
        return {vertex: self._adj_list[vertex].copy() 
                for vertex in self._adj_list}