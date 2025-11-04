"""
Análise de Grafos de Colaboração - MMDetection
Trabalho de Teoria dos Grafos - Etapa 1

Este script executa a análise completa de grafos de colaboração
do repositório open-mmlab/mmdetection conforme especificações da Etapa 1.
"""

import os
import sys
from dotenv import load_dotenv

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.graph_builder import GraphBuilder
from src.graph_visualizer import GraphVisualizer

def main():
    """Execução principal da análise"""
    
    print("="*70)
    print("ANÁLISE DE GRAFOS DE COLABORAÇÃO - MMDETECTION")
    print("Trabalho de Teoria dos Grafos - Etapa 1")
    print("="*70)
    
    # Carrega configurações
    load_dotenv()
    
    # Configurações
    REPO_OWNER = os.getenv('REPO_OWNER', 'open-mmlab')
    REPO_NAME = os.getenv('REPO_NAME', 'mmdetection')
    MAX_ISSUES = int(os.getenv('MAX_ISSUES', 500))
    MAX_PRS = int(os.getenv('MAX_PRS', 500))
    
    print(f"Repositório: {REPO_OWNER}/{REPO_NAME}")
    print(f"Máximo de issues: {MAX_ISSUES}")
    print(f"Máximo de PRs: {MAX_PRS}")
    print()
    
    # Inicializa componentes
    builder = GraphBuilder()
    visualizer = GraphVisualizer()
    
    try:
        # Etapa 1: Extração de dados
        print("ETAPA 1: Extração de dados do GitHub")
        print("-" * 40)
        
        # Tenta extrair dados do GitHub
        try:
            data = builder.extract_and_load_data(REPO_OWNER, REPO_NAME, MAX_ISSUES, MAX_PRS)
            print("✓ Dados extraídos com sucesso do GitHub")
        except Exception as e:
            print(f"✗ Erro ao extrair do GitHub: {e}")
            print("Tentando carregar dados de arquivos CSV...")
            
            # Fallback para arquivos CSV
            data = builder.load_data_from_csv(REPO_NAME)
            if not any(len(df) > 0 for df in data.values()):
                raise Exception("Nenhum dado válido encontrado. Configure o token do GitHub ou forneça arquivos CSV.")
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
            
            # Dashboard interativo
            visualizer.create_dashboard(graphs)
            print("✓ Dashboard interativo criado")
        
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
        print("1. Analise o relatório 'analysis_report.json'")
        print("2. Visualize os grafos interativos (.html)")
        print("3. Importe os arquivos .gexf no Gephi para análises avançadas")
        print("4. Use os dados CSV para análises personalizadas")
        
        print(f"\n✓ Análise concluída com sucesso!")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ ERRO: {e}")
        print("\nVerifique:")
        print("1. Token do GitHub configurado no arquivo .env")
        print("2. Conexão com a internet")
        print("3. Arquivos CSV de dados existentes")
        print("4. Dependências instaladas (requirements.txt)")
        
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)