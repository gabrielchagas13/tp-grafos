"""
Etapa 3 - Análise do Repositório Baseada em Dados
Trabalho de Teoria dos Grafos

Módulo para análise avançada de redes de colaboração.
"""

__version__ = "1.0.0"
__author__ = "Trabalho de Teoria dos Grafos"

# Importações principais
from .DataLoader import DataLoader
from .GraphAnalyzer import GraphAnalyzer
from .GraphVisualizer import GraphVisualizer
from .AbstractGraph import AbstractGraph
from .AdjacencyListGraph import AdjacencyListGraph

__all__ = [
    'DataLoader',
    'GraphAnalyzer', 
    'GraphVisualizer',
    'AbstractGraph',
    'AdjacencyListGraph'
]