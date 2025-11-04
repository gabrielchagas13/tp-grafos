"""
Análise de Grafos de Colaboração
Pacote principal para análise de grafos de colaboração em repositórios GitHub
"""

__version__ = "1.0.0"
__author__ = "Estudante de Teoria dos Grafos"
__description__ = "Análise de grafos de colaboração do repositório MMDetection"

from .github_extractor import GitHubDataExtractor
from .graph_models import (
    CollaborationNode, 
    CollaborationEdge, 
    CollaborationGraph,
    CommentGraph,
    IssueCloseGraph, 
    ReviewGraph,
    IntegratedGraph
)
from .graph_builder import GraphBuilder
from .graph_visualizer import GraphVisualizer

__all__ = [
    'GitHubDataExtractor',
    'CollaborationNode',
    'CollaborationEdge', 
    'CollaborationGraph',
    'CommentGraph',
    'IssueCloseGraph',
    'ReviewGraph',
    'IntegratedGraph',
    'GraphBuilder',
    'GraphVisualizer'
]