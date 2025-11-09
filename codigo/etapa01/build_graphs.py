"""
Construção de Grafos - MMDetection
Trabalho de Teoria dos Grafos - Etapa 2+

Este script constrói os grafos de colaboração a partir dos dados extraídos
na Etapa 1, gerando visualizações e relatórios de análise.
"""

import os
import sys
from dotenv import load_dotenv

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.graph_builder import GraphBuilder
from src.graph_visualizer import GraphVisualizer

def main():
    """Execução da construção de grafos"""
    
    print("="*70)
    print("CONSTRUÇÃO DE GRAFOS DE COLABORAÇÃO - MMDETECTION")
    print("Trabalho de Teoria dos Grafos - Etapas 2+")
    print("="*70)
    
    # Carrega configurações
    load_dotenv()
    
    # Configurações
    REPO_OWNER = os.getenv('REPO_OWNER', 'open-mmlab')
    REPO_NAME = os.getenv('REPO_NAME', 'mmdetection')
    
    print(f"Repositório: {REPO_OWNER}/{REPO_NAME}")
    print(f"Construindo grafos a partir dos dados extraídos...")
    print()
    
    # Inicializa componentes
    builder = GraphBuilder()
    visualizer = GraphVisualizer()
    
    try:
        # Carrega dados dos CSVs
        print("ETAPA 1: Carregamento dos dados")
        print("-" * 40)
        
        data = builder.load_data_from_csv(REPO_NAME)
        if not any(len(df) > 0 for df in data.values()):
            raise Exception("Nenhum dado encontrado. Execute primeiro o script main.py para extrair os dados.")
        print("✓ Dados carregados de arquivos CSV")
        
        # Etapa 2: Construção dos grafos
        print("\nETAPA 2: Construção dos grafos")
        print("-" * 40)
        
        graphs = builder.build_all_graphs()
        
        print("✓ Grafo 1 - Comentários: construído")
        print("✓ Grafo 2 - Fechamento de Issues: construído") 
        print("✓ Grafo 3 - Reviews e Merges: construído")
        print("✓ Grafo Integrado: construído")
        
        # Etapa 3: Exportação dos grafos
        print("\nETAPA 3: Exportação dos grafos")
        print("-" * 40)
        
        builder.export_all_graphs()
        print("✓ Grafos exportados em JSON e GEXF")
        
        # Etapa 4: Geração de relatórios
        print("\nETAPA 4: Geração de relatórios")
        print("-" * 40)
        
        report = builder.generate_report()
        print("✓ Relatório de análise gerado")
        
        # Etapa 5: Visualizações
        print("\nETAPA 5: Geração de visualizações")
        print("-" * 40)
        
        # Métricas dos grafos
        visualizer.plot_graph_metrics(graphs)
        print("✓ Gráfico de métricas dos grafos")
        
        # Comparação de centralidade
        visualizer.plot_centrality_comparison(graphs)
        print("✓ Comparação de métricas de centralidade")
        
        # Top colaboradores
        if "integrated" in graphs:
            visualizer.plot_top_collaborators(graphs["integrated"])
            print("✓ Gráfico de top colaboradores")
            
            # Relatório HTML completo
            html_report_path = visualizer.create_complete_html_report(graphs)
            print("✓ Relatório HTML completo criado")
        
        # Visualizações básicas de cada grafo
        for name, graph in graphs.items():
            if len(graph.nodes) > 0:  # Só visualiza se tiver dados
                try:
                    visualizer.plot_graph_basic(graph)
                    print(f"✓ Visualização básica do grafo de {name}")
                except Exception as e:
                    print(f"✗ Erro ao visualizar grafo de {name}: {e}")
        
        # Etapa 6: Resumo final
        print("\n" + "="*70)
        print("RESUMO DA ANÁLISE")
        print("="*70)
        
        builder.print_summary()
        
        # Informações sobre arquivos gerados
        print("\nARQUIVOS GERADOS:")
        print("-" * 20)
        
        # Dados
        print("Dados extraídos (pasta 'data/'):")
        data_files = [f for f in os.listdir('data') if f.endswith('.csv')]
        for file in data_files:
            print(f"  • {file}")
        
        # Outputs
        print("\nResultados da análise (pasta 'output/'):")
        output_files = [f for f in os.listdir('output')]
        for file in output_files:
            print(f"  • {file}")
        
        # Instruções finais
        print("\nPRÓXIMOS PASSOS:")
        print("-" * 20)
        print("1. Abra o arquivo 'relatorio_completo.html' no navegador")
        print("2. Analise o relatório 'analysis_report.json'")
        print("3. Visualize os grafos interativos (.html)")
        print("4. Importe os arquivos .gexf no Gephi para análises avançadas")
        print("5. Use os dados CSV para análises personalizadas")
        
        if "integrated" in graphs:
            print(f"\n🎯 RELATÓRIO PRINCIPAL:")
            print("📊 Abra 'output/relatorio_completo.html' para ver a análise completa!")
        
        print(f"\n✓ Análise concluída com sucesso!")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ ERRO: {e}")
        print("\nVerifique:")
        print("1. Execute primeiro 'python main.py' para extrair os dados")
        print("2. Arquivos CSV de dados existentes na pasta 'data/'")
        print("3. Dependências instaladas (requirements.txt)")
        
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)