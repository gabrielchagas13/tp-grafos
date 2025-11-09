"""
Classe AdjacencyListGraph
Trabalho de Teoria dos Grafos - Etapa 2

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
    
    # =================================================================
    # IMPLEMENTAÇÃO DA API OBRIGATÓRIA
    # =================================================================
    
    def getVertexCount(self) -> int:
        """
        Retorna o número de vértices do grafo.
        
        Returns:
            Número de vértices
        """
        return self._num_vertices
    
    def getEdgeCount(self) -> int:
        """
        Retorna o número de arestas do grafo.
        
        Returns:
            Número de arestas
        """
        edge_count = 0
        for vertex in self._adj_list:
            edge_count += len(self._adj_list[vertex])
        return edge_count
    
    def hasEdge(self, u: int, v: int) -> bool:
        """
        Verifica se existe aresta entre u e v.
        
        Args:
            u: Vértice origem
            v: Vértice destino
            
        Returns:
            True se existe aresta de u para v
            
        Raises:
            IndexError: Se algum índice for inválido
        """
        self._validate_vertices(u, v)
        return v in self._adj_list[u]
    
    def addEdge(self, u: int, v: int) -> None:
        """
        Adiciona aresta entre u e v (operação idempotente).
        
        Args:
            u: Vértice origem
            v: Vértice destino
            
        Raises:
            IndexError: Se algum índice for inválido
            ValueError: Se tentar criar laço (u == v)
        """
        self._validate_vertices(u, v)
        self._validate_no_self_loop(u, v)
        
        # Operação idempotente - set não duplica elementos
        self._adj_list[u].add(v)
    
    def removeEdge(self, u: int, v: int) -> None:
        """
        Remove aresta entre u e v.
        
        Args:
            u: Vértice origem
            v: Vértice destino
            
        Raises:
            IndexError: Se algum índice for inválido
        """
        self._validate_vertices(u, v)
        self._adj_list[u].discard(v)  # discard não gera erro se elemento não existir
        
        # Remove peso da aresta se existir
        if (u, v) in self._edge_weights:
            del self._edge_weights[(u, v)]
    
    def isSucessor(self, u: int, v: int) -> bool:
        """
        Verifica se v é sucessor de u.
        
        Args:
            u: Vértice origem
            v: Vértice a verificar
            
        Returns:
            True se existe aresta de u para v
            
        Raises:
            IndexError: Se algum índice for inválido
        """
        return self.hasEdge(u, v)
    
    def isPredessor(self, u: int, v: int) -> bool:
        """
        Verifica se u é predecessor de v.
        
        Args:
            u: Vértice a verificar
            v: Vértice destino
            
        Returns:
            True se existe aresta de u para v
            
        Raises:
            IndexError: Se algum índice for inválido
        """
        return self.hasEdge(u, v)
    
    def getVertexInDegree(self, u: int) -> int:
        """
        Retorna o grau de entrada do vértice u.
        
        Args:
            u: Índice do vértice
            
        Returns:
            Número de arestas que chegam em u
            
        Raises:
            IndexError: Se o índice for inválido
        """
        self._validate_vertex(u)
        
        in_degree = 0
        for vertex in self._adj_list:
            if u in self._adj_list[vertex]:
                in_degree += 1
        return in_degree
    
    def getVertexOutDegree(self, u: int) -> int:
        """
        Retorna o grau de saída do vértice u.
        
        Args:
            u: Índice do vértice
            
        Returns:
            Número de arestas que saem de u
            
        Raises:
            IndexError: Se o índice for inválido
        """
        self._validate_vertex(u)
        return len(self._adj_list[u])
    
    def isConnected(self) -> bool:
        """
        Verifica se o grafo é conectado usando DFS.
        
        Para grafo direcionado, verifica se é fracamente conectado
        (conectado quando considerado como não-direcionado).
        
        Returns:
            True se o grafo é conectado
        """
        if self._num_vertices <= 1:
            return True
            
        # DFS a partir do vértice 0
        visited = [False] * self._num_vertices
        self._dfs_connected(0, visited)
        
        # Verifica se todos os vértices foram visitados
        return all(visited)
    
    def _dfs_connected(self, vertex: int, visited: List[bool]) -> None:
        """
        DFS auxiliar para verificação de conectividade.
        
        Args:
            vertex: Vértice atual
            visited: Lista de vértices visitados
        """
        visited[vertex] = True
        
        # Visita sucessores
        for successor in self._adj_list[vertex]:
            if not visited[successor]:
                self._dfs_connected(successor, visited)
        
        # Visita predecessores (para conectividade fraca)
        for v in range(self._num_vertices):
            if not visited[v] and vertex in self._adj_list[v]:
                self._dfs_connected(v, visited)
    
    # =================================================================
    # MÉTODOS AUXILIARES
    # =================================================================
    
    def __str__(self) -> str:
        """
        Representação em string das listas de adjacência.
        
        Returns:
            String representando as listas
        """
        result = "AdjacencyListGraph:\n"
        for vertex in range(self._num_vertices):
            successors = sorted(list(self._adj_list[vertex]))
            result += f"  {vertex}: {successors}\n"
        return result
    
    def getAdjacencyList(self) -> Dict[int, Set[int]]:
        """
        Retorna cópia das listas de adjacência.
        
        Returns:
            Dicionário com as listas de adjacência
        """
        return {vertex: self._adj_list[vertex].copy() 
                for vertex in self._adj_list}
    
    def getSuccessors(self, u: int) -> Set[int]:
        """
        Retorna os sucessores do vértice u.
        
        Args:
            u: Índice do vértice
            
        Returns:
            Conjunto dos sucessores de u
            
        Raises:
            IndexError: Se o índice for inválido
        """
        self._validate_vertex(u)
        return self._adj_list[u].copy()
    
    def getPredecessors(self, u: int) -> Set[int]:
        """
        Retorna os predecessores do vértice u.
        
        Args:
            u: Índice do vértice
            
        Returns:
            Conjunto dos predecessores de u
            
        Raises:
            IndexError: Se o índice for inválido
        """
        self._validate_vertex(u)
        
        predecessors = set()
        for vertex in self._adj_list:
            if u in self._adj_list[vertex]:
                predecessors.add(vertex)
        return predecessors