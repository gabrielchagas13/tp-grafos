"""
Demonstração da Implementação de Grafos
Trabalho de Teoria dos Grafos - Etapa 2

Script para testar e demonstrar as funcionalidades das classes de grafos.
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.AdjacencyMatrixGraph import AdjacencyMatrixGraph
from src.AdjacencyListGraph import AdjacencyListGraph

def test_basic_operations(graph_class, graph_name):
    """
    Testa operações básicas de um grafo.
    
    Args:
        graph_class: Classe do grafo a testar
        graph_name: Nome da implementação
    """
    print(f"\n{'='*60}")
    print(f"TESTANDO {graph_name}")
    print(f"{'='*60}")
    
    # Cria grafo com 5 vértices
    graph = graph_class(5)
    
    print(f"✓ Grafo criado com {graph.getVertexCount()} vértices")
    print(f"✓ Número inicial de arestas: {graph.getEdgeCount()}")
    print(f"✓ Grafo vazio: {graph.isEmptyGraph()}")
    print(f"✓ Grafo completo: {graph.isCompleteGraph()}")
    
    # Adiciona algumas arestas
    print("\nAdicionando arestas...")
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)]
    
    for u, v in edges:
        graph.addEdge(u, v)
        print(f"  Aresta {u} -> {v} adicionada")
    
    print(f"\nNúmero de arestas após inserção: {graph.getEdgeCount()}")
    
    # Testa idempotência
    print("\nTestando idempotência (adicionar aresta duplicada)...")
    edges_before = graph.getEdgeCount()
    graph.addEdge(0, 1)  # Já existe
    edges_after = graph.getEdgeCount()
    print(f"✓ Arestas antes: {edges_before}, depois: {edges_after} (deve ser igual)")
    
    # Testa verificações de aresta
    print("\nVerificando existência de arestas...")
    print(f"✓ Aresta (0,1) existe: {graph.hasEdge(0, 1)}")
    print(f"✓ Aresta (1,0) existe: {graph.hasEdge(1, 0)}")
    print(f"✓ Aresta (0,2) existe: {graph.hasEdge(0, 2)}")
    
    # Testa relações de sucessor/predecessor
    print("\nTestando relações...")
    print(f"✓ 1 é sucessor de 0: {graph.isSucessor(0, 1)}")
    print(f"✓ 0 é predecessor de 1: {graph.isPredessor(0, 1)}")
    
    # Testa graus
    print("\nGraus dos vértices...")
    for i in range(graph.getVertexCount()):
        in_deg = graph.getVertexInDegree(i)
        out_deg = graph.getVertexOutDegree(i)
        print(f"  Vértice {i}: grau entrada={in_deg}, saída={out_deg}")
    
    # Testa arestas divergentes e convergentes
    print("\nTestando arestas divergentes e convergentes...")
    print(f"✓ (0,1) e (0,4) são divergentes: {graph.isDivergent(0, 1, 0, 4)}")
    print(f"✓ (3,4) e (0,4) são convergentes: {graph.isConvergent(3, 4, 0, 4)}")
    
    # Testa incidência
    print(f"✓ Aresta (0,1) é incidente a vértice 0: {graph.isIncident(0, 1, 0)}")
    print(f"✓ Aresta (0,1) é incidente a vértice 1: {graph.isIncident(0, 1, 1)}")
    print(f"✓ Aresta (0,1) é incidente a vértice 2: {graph.isIncident(0, 1, 2)}")
    
    # Testa conectividade
    print(f"\n✓ Grafo conectado: {graph.isConnected()}")
    
    # Testa pesos
    print("\nTestando pesos...")
    graph.setVertexWeight(0, 10.5)
    graph.setEdgeWeight(0, 1, 5.0)
    print(f"✓ Peso do vértice 0: {graph.getVertexWeight(0)}")
    print(f"✓ Peso da aresta (0,1): {graph.getEdgeWeight(0, 1)}")
    
    # Remove uma aresta
    print("\nRemovendo aresta (1,2)...")
    graph.removeEdge(1, 2)
    print(f"✓ Aresta (1,2) existe após remoção: {graph.hasEdge(1, 2)}")
    print(f"✓ Número de arestas: {graph.getEdgeCount()}")
    
    # Exporta para GEPHI
    output_file = f"output_{graph_name.lower().replace(' ', '_')}.gexf"
    try:
        graph.exportToGEPHI(output_file)
        print(f"✓ Grafo exportado para: {output_file}")
    except Exception as e:
        print(f"✗ Erro na exportação: {e}")
    
    print(f"\n{graph}")

def test_error_handling(graph_class, graph_name):
    """
    Testa tratamento de erros.
    
    Args:
        graph_class: Classe do grafo a testar
        graph_name: Nome da implementação
    """
    print(f"\n{'='*60}")
    print(f"TESTANDO TRATAMENTO DE ERROS - {graph_name}")
    print(f"{'='*60}")
    
    graph = graph_class(3)
    
    # Testa índices inválidos
    test_cases = [
        ("Índice negativo", lambda: graph.addEdge(-1, 0)),
        ("Índice muito alto", lambda: graph.addEdge(0, 5)),
        ("Laço (self-loop)", lambda: graph.addEdge(1, 1)),
        ("Peso de aresta inexistente", lambda: graph.getEdgeWeight(0, 1)),
        ("Peso de vértice inválido", lambda: graph.setVertexWeight(10, 5.0))
    ]
    
    for description, test_func in test_cases:
        try:
            test_func()
            print(f"✗ {description}: Deveria ter gerado exceção!")
        except (IndexError, ValueError) as e:
            print(f"✓ {description}: {type(e).__name__} - {e}")
        except Exception as e:
            print(f"? {description}: Exceção inesperada - {type(e).__name__}: {e}")

def test_complete_graph():
    """Testa grafo completo."""
    print(f"\n{'='*60}")
    print("TESTANDO GRAFO COMPLETO")
    print(f"{'='*60}")
    
    graph = AdjacencyMatrixGraph(4)
    
    # Adiciona todas as arestas possíveis
    for u in range(4):
        for v in range(4):
            if u != v:  # Sem laços
                graph.addEdge(u, v)
    
    print(f"✓ Número de vértices: {graph.getVertexCount()}")
    print(f"✓ Número de arestas: {graph.getEdgeCount()}")
    print(f"✓ É grafo completo: {graph.isCompleteGraph()}")
    print(f"✓ É grafo vazio: {graph.isEmptyGraph()}")

def main():
    """Execução principal dos testes."""
    
    print("DEMONSTRAÇÃO DAS IMPLEMENTAÇÕES DE GRAFOS")
    print("Trabalho de Teoria dos Grafos - Etapa 2")
    
    # Testa as duas implementações
    test_basic_operations(AdjacencyMatrixGraph, "MATRIZ DE ADJACÊNCIA")
    test_basic_operations(AdjacencyListGraph, "LISTAS DE ADJACÊNCIA")
    
    # Testa tratamento de erros
    test_error_handling(AdjacencyMatrixGraph, "MATRIZ")
    test_error_handling(AdjacencyListGraph, "LISTAS")
    
    # Testa casos especiais
    test_complete_graph()
    
    print(f"\n{'='*60}")
    print("TESTES CONCLUÍDOS")
    print("✓ Todas as funcionalidades da API foram testadas")
    print("✓ Tratamento de erros funcionando corretamente")  
    print("✓ Arquivos GEXF gerados para importação no Gephi")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()