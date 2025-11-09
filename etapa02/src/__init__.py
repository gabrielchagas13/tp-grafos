"""
Módulo de Grafos - Etapa 2
Trabalho de Teoria dos Grafos

Estrutura de classes para implementação de grafos com diferentes representações.
"""

from .AbstractGraph import AbstractGraph
from .AdjacencyMatrixGraph import AdjacencyMatrixGraph
from .AdjacencyListGraph import AdjacencyListGraph

__all__ = [
    'AbstractGraph',
    'AdjacencyMatrixGraph', 
    'AdjacencyListGraph'
]

__version__ = '1.0.0'
__author__ = 'Trabalho de Teoria dos Grafos - Etapa 2'