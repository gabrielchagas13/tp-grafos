"""
Testes Unitários para as Classes de Grafos
Trabalho de Teoria dos Grafos - Etapa 2

Testes rigorosos para validar a corretude da implementação.
"""

import unittest
import sys
import os

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.AdjacencyMatrixGraph import AdjacencyMatrixGraph
from src.AdjacencyListGraph import AdjacencyListGraph

class TestGraphImplementations(unittest.TestCase):
    """
    Classe de testes para ambas as implementações de grafos.
    """
    
    def setUp(self):
        """Configura testes com ambas as implementações."""
        self.implementations = [
            ("AdjacencyMatrixGraph", AdjacencyMatrixGraph),
            ("AdjacencyListGraph", AdjacencyListGraph)
        ]
    
    def test_constructor_valid(self):
        """Testa construtores com valores válidos."""
        for name, graph_class in self.implementations:
            with self.subTest(implementation=name):
                graph = graph_class(5)
                self.assertEqual(graph.getVertexCount(), 5)
                self.assertEqual(graph.getEdgeCount(), 0)
                self.assertTrue(graph.isEmptyGraph())
                self.assertFalse(graph.isCompleteGraph())
    
    def test_constructor_invalid(self):
        """Testa construtores com valores inválidos."""
        for name, graph_class in self.implementations:
            with self.subTest(implementation=name):
                with self.assertRaises(ValueError):
                    graph_class(0)
                with self.assertRaises(ValueError):
                    graph_class(-1)
    
    def test_add_edge_valid(self):
        """Testa adição de arestas válidas."""
        for name, graph_class in self.implementations:
            with self.subTest(implementation=name):
                graph = graph_class(3)
                
                # Adiciona aresta válida
                graph.addEdge(0, 1)
                self.assertTrue(graph.hasEdge(0, 1))
                self.assertEqual(graph.getEdgeCount(), 1)
                
                # Testa idempotência
                graph.addEdge(0, 1)
                self.assertEqual(graph.getEdgeCount(), 1)
    
    def test_add_edge_invalid(self):
        """Testa adição de arestas inválidas."""
        for name, graph_class in self.implementations:
            with self.subTest(implementation=name):
                graph = graph_class(3)
                
                # Índices inválidos
                with self.assertRaises(IndexError):
                    graph.addEdge(-1, 0)
                with self.assertRaises(IndexError):
                    graph.addEdge(0, 5)
                
                # Laço (self-loop)
                with self.assertRaises(ValueError):
                    graph.addEdge(1, 1)
    
    def test_remove_edge(self):
        """Testa remoção de arestas."""
        for name, graph_class in self.implementations:
            with self.subTest(implementation=name):
                graph = graph_class(3)
                
                # Adiciona e remove aresta
                graph.addEdge(0, 1)
                self.assertTrue(graph.hasEdge(0, 1))
                
                graph.removeEdge(0, 1)
                self.assertFalse(graph.hasEdge(0, 1))
                self.assertEqual(graph.getEdgeCount(), 0)
                
                # Remove aresta inexistente (não deve dar erro)
                graph.removeEdge(1, 2)
    
    def test_successor_predecessor(self):
        """Testa relações de sucessor e predecessor."""
        for name, graph_class in self.implementations:
            with self.subTest(implementation=name):
                graph = graph_class(3)
                graph.addEdge(0, 1)
                
                self.assertTrue(graph.isSucessor(0, 1))
                self.assertTrue(graph.isPredessor(0, 1))
                self.assertFalse(graph.isSucessor(1, 0))
                self.assertFalse(graph.isPredessor(1, 0))
    
    def test_degrees(self):
        """Testa cálculo de graus."""
        for name, graph_class in self.implementations:
            with self.subTest(implementation=name):
                graph = graph_class(4)
                
                # Grafo: 0->1, 0->2, 1->2, 2->3
                edges = [(0, 1), (0, 2), (1, 2), (2, 3)]
                for u, v in edges:
                    graph.addEdge(u, v)
                
                # Graus de saída
                self.assertEqual(graph.getVertexOutDegree(0), 2)  # 0->1, 0->2
                self.assertEqual(graph.getVertexOutDegree(1), 1)  # 1->2
                self.assertEqual(graph.getVertexOutDegree(2), 1)  # 2->3
                self.assertEqual(graph.getVertexOutDegree(3), 0)  # sem saída
                
                # Graus de entrada
                self.assertEqual(graph.getVertexInDegree(0), 0)   # sem entrada
                self.assertEqual(graph.getVertexInDegree(1), 1)   # 0->1
                self.assertEqual(graph.getVertexInDegree(2), 2)   # 0->2, 1->2
                self.assertEqual(graph.getVertexInDegree(3), 1)   # 2->3
    
    def test_divergent_convergent(self):
        """Testa arestas divergentes e convergentes."""
        for name, graph_class in self.implementations:
            with self.subTest(implementation=name):
                graph = graph_class(4)
                
                # Arestas divergentes: 0->1, 0->2
                graph.addEdge(0, 1)
                graph.addEdge(0, 2)
                self.assertTrue(graph.isDivergent(0, 1, 0, 2))
                
                # Arestas convergentes: 1->3, 2->3
                graph.addEdge(1, 3)
                graph.addEdge(2, 3)
                self.assertTrue(graph.isConvergent(1, 3, 2, 3))
                
                # Arestas não divergentes/convergentes
                self.assertFalse(graph.isDivergent(0, 1, 1, 3))
                self.assertFalse(graph.isConvergent(0, 1, 0, 2))
    
    def test_incident(self):
        """Testa incidência de arestas."""
        for name, graph_class in self.implementations:
            with self.subTest(implementation=name):
                graph = graph_class(3)
                graph.addEdge(0, 1)
                
                # Aresta (0,1) é incidente aos vértices 0 e 1
                self.assertTrue(graph.isIncident(0, 1, 0))
                self.assertTrue(graph.isIncident(0, 1, 1))
                self.assertFalse(graph.isIncident(0, 1, 2))
    
    def test_vertex_weights(self):
        """Testa pesos de vértices."""
        for name, graph_class in self.implementations:
            with self.subTest(implementation=name):
                graph = graph_class(3)
                
                # Peso padrão
                self.assertEqual(graph.getVertexWeight(0), 0.0)
                
                # Define e recupera peso
                graph.setVertexWeight(0, 10.5)
                self.assertEqual(graph.getVertexWeight(0), 10.5)
                
                # Índice inválido
                with self.assertRaises(IndexError):
                    graph.setVertexWeight(5, 1.0)
    
    def test_edge_weights(self):
        """Testa pesos de arestas."""
        for name, graph_class in self.implementations:
            with self.subTest(implementation=name):
                graph = graph_class(3)
                graph.addEdge(0, 1)
                
                # Peso padrão
                self.assertEqual(graph.getEdgeWeight(0, 1), 1.0)
                
                # Define e recupera peso
                graph.setEdgeWeight(0, 1, 5.5)
                self.assertEqual(graph.getEdgeWeight(0, 1), 5.5)
                
                # Aresta inexistente
                with self.assertRaises(ValueError):
                    graph.getEdgeWeight(1, 2)
                with self.assertRaises(ValueError):
                    graph.setEdgeWeight(1, 2, 3.0)
    
    def test_complete_graph(self):
        """Testa grafo completo."""
        for name, graph_class in self.implementations:
            with self.subTest(implementation=name):
                graph = graph_class(3)
                
                # Inicialmente não é completo
                self.assertFalse(graph.isCompleteGraph())
                
                # Adiciona todas as arestas (sem laços)
                for u in range(3):
                    for v in range(3):
                        if u != v:
                            graph.addEdge(u, v)
                
                self.assertTrue(graph.isCompleteGraph())
                self.assertEqual(graph.getEdgeCount(), 6)  # 3*(3-1)
    
    def test_connected_graph(self):
        """Testa conectividade do grafo."""
        for name, graph_class in self.implementations:
            with self.subTest(implementation=name):
                graph = graph_class(4)
                
                # Grafo desconectado
                graph.addEdge(0, 1)
                graph.addEdge(2, 3)
                self.assertFalse(graph.isConnected())
                
                # Conecta os componentes
                graph.addEdge(1, 2)
                self.assertTrue(graph.isConnected())
    
    def test_gephi_export(self):
        """Testa exportação para Gephi."""
        for name, graph_class in self.implementations:
            with self.subTest(implementation=name):
                graph = graph_class(3)
                graph.addEdge(0, 1)
                graph.addEdge(1, 2)
                graph.setVertexWeight(0, 5.0)
                graph.setEdgeWeight(0, 1, 2.5)
                
                filename = f"test_{name.lower()}.gexf"
                
                # Não deve gerar exceção
                try:
                    graph.exportToGEPHI(filename)
                    # Verifica se arquivo foi criado
                    self.assertTrue(os.path.exists(filename))
                    
                    # Remove arquivo de teste
                    if os.path.exists(filename):
                        os.remove(filename)
                        
                except Exception as e:
                    self.fail(f"Exportação falhou: {e}")

class TestSpecificImplementations(unittest.TestCase):
    """
    Testes específicos para cada implementação.
    """
    
    def test_matrix_representation(self):
        """Testa representação específica da matriz."""
        graph = AdjacencyMatrixGraph(3)
        graph.addEdge(0, 1)
        graph.addEdge(1, 2)
        
        matrix = graph.getAdjacencyMatrix()
        self.assertFalse(matrix[0][0])  # Sem laço
        self.assertTrue(matrix[0][1])   # Aresta 0->1
        self.assertFalse(matrix[1][0])  # Sem aresta 1->0
        self.assertTrue(matrix[1][2])   # Aresta 1->2
    
    def test_list_representation(self):
        """Testa representação específica das listas."""
        graph = AdjacencyListGraph(3)
        graph.addEdge(0, 1)
        graph.addEdge(0, 2)
        
        successors_0 = graph.getSuccessors(0)
        self.assertEqual(successors_0, {1, 2})
        
        predecessors_1 = graph.getPredecessors(1)
        self.assertEqual(predecessors_1, {0})
        
        adj_list = graph.getAdjacencyList()
        self.assertEqual(adj_list[0], {1, 2})
        self.assertEqual(adj_list[1], set())
        self.assertEqual(adj_list[2], set())

if __name__ == '__main__':
    # Executa os testes
    unittest.main(verbosity=2)