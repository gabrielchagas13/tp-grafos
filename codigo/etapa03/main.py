"""
Script Principal da Etapa 3
Trabalho de Teoria dos Grafos - Análise de Repositório Baseada em Dados

Análise completa da rede de colaboração do repositório mmdetection.
"""

import os
import sys
import json
from typing import Dict, List

# Adiciona diretório src ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.DataLoader import DataLoader
from src.GraphAnalyzer import GraphAnalyzer  
from src.GraphVisualizer import GraphVisualizer

def main():
    """
    Execução principal da análise.
    """
    print("=" * 80)
    print("ETAPA 3 - ANÁLISE DO REPOSITÓRIO BASEADA EM DADOS")
    print("Trabalho de Teoria dos Grafos")
    print("Repositório: mmdetection")
    print("=" * 80)
    
    # Configurações
    data_dir = "../etapa01/data"
    output_dir = "./output"
    
    # Cria diretório de saída
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. CARREGAMENTO DOS DADOS
    print("\n🔄 1. CARREGANDO DADOS DA ETAPA 1...")
    print("-" * 50)
    
    loader = DataLoader(data_dir)
    data = loader.load_csv_data()
    
    # Verifica se os dados foram carregados
    total_records = sum(len(records) for records in data.values())
    if total_records == 0:
        print("❌ ERRO: Nenhum dado encontrado!")
        print("   Certifique-se de que a Etapa 1 foi executada e gerou os CSVs.")
        return
    
    print(f"✅ Total de registros carregados: {total_records}")
    
    # 2. CONSTRUÇÃO DO GRAFO
    print("\n🔄 2. CONSTRUINDO GRAFO DE COLABORAÇÃO...")
    print("-" * 50)
    
    graph = loader.build_collaboration_graph(data)
    user_mapping = loader.get_user_mapping()
    
    if graph.getVertexCount() == 0:
        print("❌ ERRO: Grafo vazio!")
        return
    
    # 3. ANÁLISE DO GRAFO
    print("\n🔄 3. EXECUTANDO ANÁLISES...")
    print("-" * 50)
    
    analyzer = GraphAnalyzer(graph)
    
    # Análise de centralidade
    print("   📊 Calculando métricas de centralidade...")
    centrality_results = {
        'degree_centrality': analyzer.calculate_degree_centrality(),
        'betweenness_centrality': analyzer.calculate_betweenness_centrality(),
        'closeness_centrality': analyzer.calculate_closeness_centrality(),
        'pagerank_centrality': analyzer.calculate_pagerank(),
        'eigenvector_centrality': analyzer.calculate_eigenvector_centrality()
    }
    
    # Métricas da rede
    print("   📊 Calculando métricas da rede...")
    
    # Calcula grau médio manualmente
    total_degree = sum(graph.getVertexInDegree(v) + graph.getVertexOutDegree(v) 
                      for v in range(graph.getVertexCount()))
    average_degree = total_degree / graph.getVertexCount() if graph.getVertexCount() > 0 else 0
    
    network_metrics = {
        'vertex_count': graph.getVertexCount(),
        'edge_count': graph.getEdgeCount(),
        'density': analyzer.calculate_network_density(),
        'average_degree': average_degree,
        'average_clustering': analyzer.calculate_average_clustering_coefficient(),
        'assortativity': analyzer.calculate_assortativity()
    }
    
    # Análise de comunidades - implementação básica
    print("   📊 Analisando estrutura comunitária...")
    
    community_metrics = {
        'modularity': analyzer.calculate_modularity_simple(),
        'bridging_ties_ratio': analyzer.calculate_bridging_ties_ratio()
    }
    
    # 4. VISUALIZAÇÕES
    print("\n🔄 4. GERANDO VISUALIZAÇÕES...")
    print("-" * 50)
    
    visualizer = GraphVisualizer(output_dir)
    
    # Gráfico de comparação de centralidades
    visualizer.plot_centrality_comparison(
        centrality_results, user_mapping, 
        save_path="centralidade_comparacao.png"
    )
    
    # Gráfico de métricas da rede  
    visualizer.plot_network_metrics(
        network_metrics,
        save_path="metricas_rede.png"
    )
    
    # Distribuição de graus
    visualizer.plot_degree_distribution(
        graph, user_mapping,
        save_path="distribuicao_graus.png"
    )
    
    # Análise comunitária
    visualizer.plot_community_analysis(
        community_metrics,
        save_path="analise_comunidades.png"
    )
    
    # NOVOS GRÁFICOS ESPECÍFICOS PARA GRAFOS DIRECIONADOS
    print("   📊 Gerando visualizações específicas para grafos direcionados...")
    
    # Estrutura do grafo direcionado
    visualizer.plot_directed_graph_structure(
        graph, user_mapping, centrality_results,
        save_path="grafo_direcionado.png"
    )
    
    # Detecção detalhada de comunidades e bridging ties
    visualizer.plot_community_detection_detailed(
        graph, analyzer, user_mapping,
        save_path="deteccao_comunidades.png"
    )
    
    # Análise de fluxo direcionado
    visualizer.plot_directed_flow_analysis(
        graph, user_mapping, centrality_results,
        save_path="analise_fluxo_direcionado.png"
    )
    
    # NOVOS GRÁFICOS DE REDE VISUAL
    print("   🎨 Gerando visualizações da estrutura da rede...")
    
    # Obtém comunidades para visualização
    communities = analyzer._detect_simple_communities()
    
    # Visualização manual do grafo da rede
    visualizer.plot_network_graph_manual(
        graph, user_mapping, centrality_results, communities,
        save_path="rede_grafo_manual.png"
    )
    
    # Análise detalhada de bridging ties
    visualizer.plot_bridging_ties_analysis(
        graph, analyzer, user_mapping,
        save_path="bridging_ties_detalhado.png"
    )
    
    # 5. RELATÓRIOS
    print("\n🔄 5. GERANDO RELATÓRIOS...")
    print("-" * 50)
    
    # Resultados completos
    complete_results = {
        'centrality': centrality_results,
        'network_metrics': network_metrics,
        'community_metrics': community_metrics,
        'metadata': {
            'total_users': len(user_mapping),
            'data_files_loaded': list(data.keys()),
            'total_records_processed': total_records
        }
    }
    
    # Salva resultados completos
    results_path = os.path.join(output_dir, "resultados_completos.json")
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(complete_results, f, indent=2, ensure_ascii=False)
    
    # Relatório resumo
    summary_report = visualizer.create_summary_report(
        complete_results, user_mapping,
        save_path="relatorio_resumo.json"
    )
    
    # 6. RESUMO EXECUTIVO
    print("\n🔄 6. RESUMO EXECUTIVO...")
    print("-" * 50)
    
    print(f"\n📊 ESTATÍSTICAS GERAIS:")
    print(f"   • Desenvolvedores únicos: {network_metrics['vertex_count']}")
    print(f"   • Conexões de colaboração: {network_metrics['edge_count']}")
    print(f"   • Densidade da rede: {network_metrics['density']:.4f}")
    print(f"   • Grau médio: {network_metrics['average_degree']:.2f}")
    
    print(f"\n🔗 ESTRUTURA DA REDE:")
    print(f"   • Coeficiente de clustering: {network_metrics['average_clustering']:.4f}")
    print(f"   • Assortatividade: {network_metrics['assortativity']:.4f}")
    print(f"   • Modularidade: {community_metrics['modularity']:.4f}")
    
    # Top 5 usuários por centralidade
    print(f"\n⭐ TOP 5 DESENVOLVEDORES (por centralidade de grau):")
    degree_centrality = centrality_results['degree_centrality']
    top_users = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    
    for i, (user_id, centrality) in enumerate(top_users, 1):
        username = user_mapping.get(int(user_id), f"user_{user_id}")
        print(f"   {i}. {username} (centralidade: {centrality:.4f})")
    
    # Insights automáticos
    insights = summary_report.get('key_insights', [])
    if insights:
        print(f"\n💡 INSIGHTS PRINCIPAIS:")
        for insight in insights[:5]:  # Mostra apenas os 5 primeiros
            print(f"   • {insight}")
    
    print("\n✅ ANÁLISE CONCLUÍDA!")
    print(f"   📁 Resultados salvos em: {os.path.abspath(output_dir)}")
    print(f"   📊 Gráficos Básicos: centralidade_comparacao.png, metricas_rede.png")
    print(f"   📊 Gráficos Básicos: distribuicao_graus.png, analise_comunidades.png")
    print(f"   🎯 Gráficos Direcionados: grafo_direcionado.png, deteccao_comunidades.png")
    print(f"   🎯 Gráficos Direcionados: analise_fluxo_direcionado.png")
    print(f"   🎨 Gráficos de Rede: rede_grafo_manual.png, bridging_ties_detalhado.png")
    print(f"   📋 Relatórios: resultados_completos.json, relatorio_resumo.json")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Análise interrompida pelo usuário.")
    except Exception as e:
        print(f"\n❌ ERRO durante a análise: {e}")
        import traceback
        traceback.print_exc()