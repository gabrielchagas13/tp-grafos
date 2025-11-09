"""
Classe AdjacencyMatrixGraph
Trabalho de Teoria dos Grafos - Etapa 2

Implementação da API utilizando matriz de adjacência.
"""

from typing import List
from .AbstractGraph import AbstractGraph

class AdjacencyMatrixGraph(AbstractGraph):
    """
    Implementação de grafo usando matriz de adjacência.
    
    A matriz é uma lista de listas onde matrix[u][v] = True
    indica que existe aresta do vértice u para o vértice v.
    """
    
    def __init__(self, num_vertices: int):
        """
        Inicializa grafo com matriz de adjacência.
        
        Args:
            num_vertices: Número de vértices do grafo
            
        Raises:
            ValueError: Se num_vertices <= 0
        """
        super().__init__(num_vertices)
        
        # Inicializa matriz de adjacência (False = sem aresta)
        self._matrix: List[List[bool]] = [
            [False for _ in range(num_vertices)] 
            for _ in range(num_vertices)
        ]
    
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
        for i in range(self._num_vertices):
            for j in range(self._num_vertices):
                if self._matrix[i][j]:
                    edge_count += 1
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
        return self._matrix[u][v]
    
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
        
        # Operação idempotente - não duplica aresta
        self._matrix[u][v] = True
    
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
        self._matrix[u][v] = False
        
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
        for i in range(self._num_vertices):
            if self._matrix[i][u]:
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
        
        out_degree = 0
        for j in range(self._num_vertices):
            if self._matrix[u][j]:
                out_degree += 1
        return out_degree
    
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
        
        # Visita todos os vizinhos (considerando grafo não-direcionado)
        for i in range(self._num_vertices):
            if not visited[i] and (self._matrix[vertex][i] or self._matrix[i][vertex]):
                self._dfs_connected(i, visited)
    
    # =================================================================
    # MÉTODOS AUXILIARES
    # =================================================================
    
    def __str__(self) -> str:
        """
        Representação em string da matriz de adjacência.
        
        Returns:
            String representando a matriz
        """
        result = "AdjacencyMatrixGraph:\n"
        result += "  "
        
        # Cabeçalho das colunas
        for j in range(self._num_vertices):
            result += f"{j:3}"
        result += "\n"
        
        # Linhas da matriz
        for i in range(self._num_vertices):
            result += f"{i}: "
            for j in range(self._num_vertices):
                result += f"{int(self._matrix[i][j]):3}"
            result += "\n"
            
        return result
    
    def getAdjacencyMatrix(self) -> List[List[bool]]:
        """
        Retorna cópia da matriz de adjacência.
        
        Returns:
            Matriz de adjacência como lista de listas
        """
        return [row[:] for row in self._matrix]