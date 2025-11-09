"""
Classe Abstrata AbstractGraph
Trabalho de Teoria dos Grafos - Etapa 2

Define a API comum, atributos compartilhados (rótulos e pesos de vértices),
e métodos auxiliares para implementações de grafos.
"""

from abc import ABC, abstractmethod
from typing import Dict, List

class AbstractGraph(ABC):
    """
    Classe abstrata que define a API comum para implementações de grafos.
    
    Atributos compartilhados:
    - vertex_labels: rótulos dos vértices
    - vertex_weights: pesos dos vértices  
    - edge_weights: pesos das arestas
    """
    
    def __init__(self, num_vertices: int):
        """
        Inicializa o grafo com número especificado de vértices.
        
        Args:
            num_vertices: Número de vértices do grafo
            
        Raises:
            ValueError: Se num_vertices <= 0
        """
        if num_vertices <= 0:
            raise ValueError("Número de vértices deve ser maior que zero")
            
        self._num_vertices = num_vertices
        self._vertex_labels: Dict[int, str] = {}
        self._vertex_weights: Dict[int, float] = {}
        self._edge_weights: Dict[tuple, float] = {}
        
    def _validate_vertex(self, vertex: int) -> None:
        """
        Valida se o índice do vértice é válido.
        
        Args:
            vertex: Índice do vértice
            
        Raises:
            IndexError: Se o índice for inválido
        """
        if vertex < 0 or vertex >= self._num_vertices:
            raise IndexError(f"Índice de vértice inválido: {vertex}. Deve estar entre 0 e {self._num_vertices-1}")
    
    def _validate_vertices(self, u: int, v: int) -> None:
        """
        Valida se os índices dos vértices são válidos.
        
        Args:
            u: Índice do primeiro vértice
            v: Índice do segundo vértice
            
        Raises:
            IndexError: Se algum índice for inválido
        """
        self._validate_vertex(u)
        self._validate_vertex(v)
        
    def _validate_no_self_loop(self, u: int, v: int) -> None:
        """
        Valida que não há laço (self-loop).
        
        Args:
            u: Índice do primeiro vértice
            v: Índice do segundo vértice
            
        Raises:
            ValueError: Se u == v (laço)
        """
        if u == v:
            raise ValueError("Grafos simples não permitem laços (self-loops)")

    # =================================================================
    # API OBRIGATÓRIA - MÉTODOS ABSTRATOS
    # =================================================================
    
    @abstractmethod
    def getVertexCount(self) -> int:
        """Retorna o número de vértices do grafo."""
        pass
    
    @abstractmethod  
    def getEdgeCount(self) -> int:
        """Retorna o número de arestas do grafo."""
        pass
    
    @abstractmethod
    def hasEdge(self, u: int, v: int) -> bool:
        """Verifica se existe aresta entre u e v."""
        pass
    
    @abstractmethod
    def addEdge(self, u: int, v: int) -> None:
        """Adiciona aresta entre u e v (idempotente)."""
        pass
    
    @abstractmethod
    def removeEdge(self, u: int, v: int) -> None:
        """Remove aresta entre u e v."""
        pass
        
    @abstractmethod
    def isSucessor(self, u: int, v: int) -> bool:
        """Verifica se v é sucessor de u."""
        pass
    
    @abstractmethod
    def isPredessor(self, u: int, v: int) -> bool:
        """Verifica se u é predecessor de v."""
        pass
    
    @abstractmethod
    def getVertexInDegree(self, u: int) -> int:
        """Retorna o grau de entrada do vértice u."""
        pass
    
    @abstractmethod
    def getVertexOutDegree(self, u: int) -> int:
        """Retorna o grau de saída do vértice u."""
        pass
    
    @abstractmethod
    def isConnected(self) -> bool:
        """Verifica se o grafo é conectado."""
        pass
    
    # =================================================================
    # API OBRIGATÓRIA - MÉTODOS CONCRETOS
    # =================================================================
    
    def isDivergent(self, u1: int, v1: int, u2: int, v2: int) -> bool:
        """
        Verifica se duas arestas são divergentes (mesmo vértice de origem).
        
        Args:
            u1, v1: Primeira aresta
            u2, v2: Segunda aresta
            
        Returns:
            True se u1 == u2 e as arestas existem
        """
        self._validate_vertices(u1, v1)
        self._validate_vertices(u2, v2)
        
        return (u1 == u2 and 
                self.hasEdge(u1, v1) and 
                self.hasEdge(u2, v2))
    
    def isConvergent(self, u1: int, v1: int, u2: int, v2: int) -> bool:
        """
        Verifica se duas arestas são convergentes (mesmo vértice de destino).
        
        Args:
            u1, v1: Primeira aresta
            u2, v2: Segunda aresta
            
        Returns:
            True se v1 == v2 e as arestas existem
        """
        self._validate_vertices(u1, v1)
        self._validate_vertices(u2, v2)
        
        return (v1 == v2 and 
                self.hasEdge(u1, v1) and 
                self.hasEdge(u2, v2))
    
    def isIncident(self, u: int, v: int, x: int) -> bool:
        """
        Verifica se a aresta (u,v) é incidente ao vértice x.
        
        Args:
            u, v: Vértices da aresta
            x: Vértice a verificar incidência
            
        Returns:
            True se x == u ou x == v e a aresta existe
        """
        self._validate_vertices(u, v)
        self._validate_vertex(x)
        
        return (self.hasEdge(u, v) and (x == u or x == v))
    
    def setVertexWeight(self, v: int, w: float) -> None:
        """
        Define o peso do vértice v.
        
        Args:
            v: Índice do vértice
            w: Peso do vértice
            
        Raises:
            IndexError: Se o índice for inválido
        """
        self._validate_vertex(v)
        self._vertex_weights[v] = w
    
    def getVertexWeight(self, v: int) -> float:
        """
        Retorna o peso do vértice v.
        
        Args:
            v: Índice do vértice
            
        Returns:
            Peso do vértice (0.0 se não definido)
            
        Raises:
            IndexError: Se o índice for inválido
        """
        self._validate_vertex(v)
        return self._vertex_weights.get(v, 0.0)
    
    def setEdgeWeight(self, u: int, v: int, w: float) -> None:
        """
        Define o peso da aresta (u,v).
        
        Args:
            u: Vértice origem
            v: Vértice destino
            w: Peso da aresta
            
        Raises:
            IndexError: Se algum índice for inválido
            ValueError: Se a aresta não existir
        """
        self._validate_vertices(u, v)
        if not self.hasEdge(u, v):
            raise ValueError(f"Aresta ({u},{v}) não existe")
        self._edge_weights[(u, v)] = w
    
    def getEdgeWeight(self, u: int, v: int) -> float:
        """
        Retorna o peso da aresta (u,v).
        
        Args:
            u: Vértice origem  
            v: Vértice destino
            
        Returns:
            Peso da aresta (1.0 se não definido)
            
        Raises:
            IndexError: Se algum índice for inválido
            ValueError: Se a aresta não existir
        """
        self._validate_vertices(u, v)
        if not self.hasEdge(u, v):
            raise ValueError(f"Aresta ({u},{v}) não existe")
        return self._edge_weights.get((u, v), 1.0)
    
    def isEmptyGraph(self) -> bool:
        """
        Verifica se o grafo é vazio (sem arestas).
        
        Returns:
            True se não há arestas
        """
        return self.getEdgeCount() == 0
    
    def isCompleteGraph(self) -> bool:
        """
        Verifica se o grafo é completo.
        
        Returns:
            True se existe aresta entre todos os pares de vértices
        """
        n = self.getVertexCount()
        max_edges = n * (n - 1)  # Grafo direcionado sem laços
        return self.getEdgeCount() == max_edges
    
    # =================================================================
    # EXPORTAÇÃO PARA GEPHI
    # =================================================================
    
    def exportToGEPHI(self, path: str) -> None:
        """
        Exporta o grafo para formato GEXF (aceito pelo Gephi).
        Implementação manual sem dependências externas.
        
        Args:
            path: Caminho do arquivo a ser criado
            
        Raises:
            IOError: Se não conseguir escrever o arquivo
        """
        try:
            # Constrói o XML manualmente como string
            xml_content = []
            xml_content.append('<?xml version="1.0" encoding="UTF-8"?>')
            xml_content.append('<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">')
            xml_content.append('  <graph mode="static" defaultedgetype="directed">')
            
            # Adiciona nós
            xml_content.append('    <nodes>')
            for i in range(self.getVertexCount()):
                weight = self.getVertexWeight(i)
                if weight != 0.0:
                    xml_content.append(f'      <node id="{i}" label="{i}" weight="{weight}"/>')
                else:
                    xml_content.append(f'      <node id="{i}" label="{i}"/>')
            xml_content.append('    </nodes>')
            
            # Adiciona arestas
            xml_content.append('    <edges>')
            edge_id = 0
            
            for u in range(self.getVertexCount()):
                for v in range(self.getVertexCount()):
                    if self.hasEdge(u, v):
                        weight = self.getEdgeWeight(u, v)
                        if weight != 1.0:
                            xml_content.append(f'      <edge id="{edge_id}" source="{u}" target="{v}" weight="{weight}"/>')
                        else:
                            xml_content.append(f'      <edge id="{edge_id}" source="{u}" target="{v}"/>')
                        edge_id += 1
            
            xml_content.append('    </edges>')
            xml_content.append('  </graph>')
            xml_content.append('</gexf>')
            
            # Salva arquivo
            with open(path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(xml_content))
                
        except Exception as e:
            raise IOError(f"Erro ao exportar para GEPHI: {e}")