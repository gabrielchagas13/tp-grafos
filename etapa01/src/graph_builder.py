"""
Graph Builder
Módulo principal para construção e análise dos grafos de colaboração
"""

import pandas as pd
import os
from typing import Dict, List
import json
from src.github_extractor import GitHubDataExtractor
from src.graph_models import CommentGraph, IssueCloseGraph, ReviewGraph, IntegratedGraph

class GraphBuilder:
    """Classe principal para construção e análise dos grafos"""
    
    def __init__(self, data_dir: str = "data", output_dir: str = "output"):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.graphs = {}
        self.data = {}
        
        # Cria diretórios se não existirem
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
    
    def load_data_from_csv(self, repo_name: str) -> Dict[str, pd.DataFrame]:
        """Carrega dados dos arquivos CSV"""
        print("Carregando dados dos arquivos CSV...")
        
        data = {}
        
        # Arquivos esperados
        files = {
            "issues": f"issues_{repo_name}.csv",
            "pull_requests": f"pull_requests_{repo_name}.csv",
            "issue_comments": f"issue_comments_{repo_name}.csv",
            "pr_reviews": f"pr_reviews_{repo_name}.csv",
            "pr_comments": f"pr_comments_{repo_name}.csv"
        }
        
        for key, filename in files.items():
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                data[key] = pd.read_csv(filepath)
                print(f"  - {key}: {len(data[key])} registros")
            else:
                print(f"  - AVISO: {filename} não encontrado")
                data[key] = pd.DataFrame()
        
        self.data = data
        return data
    
    def extract_and_load_data(self, repo_owner: str, repo_name: str, 
                             max_issues: int = 500, max_prs: int = 500) -> Dict[str, pd.DataFrame]:
        """Extrai dados do GitHub e carrega em memória"""
        print("Extraindo dados do GitHub...")
        
        extractor = GitHubDataExtractor(repo_owner, repo_name)
        self.data = extractor.extract_all_data(max_issues, max_prs)
        
        return self.data
    
    def build_all_graphs(self) -> Dict[str, object]:
        """Constrói todos os grafos a partir dos dados carregados"""
        if not self.data:
            raise ValueError("Nenhum dado carregado. Execute load_data_from_csv() ou extract_and_load_data() primeiro.")
        
        print("Construindo todos os grafos...")
        
        # Verifica se temos dados mínimos
        issues_df = self.data.get("issues", pd.DataFrame())
        prs_df = self.data.get("pull_requests", pd.DataFrame())
        issue_comments_df = self.data.get("issue_comments", pd.DataFrame())
        pr_comments_df = self.data.get("pr_comments", pd.DataFrame())
        pr_reviews_df = self.data.get("pr_reviews", pd.DataFrame())
        
        print(f"Dados disponíveis: Issues={len(issues_df)}, PRs={len(prs_df)}, "
              f"Issue Comments={len(issue_comments_df)}, PR Comments={len(pr_comments_df)}, "
              f"Reviews={len(pr_reviews_df)}")
        
        # Grafo 1: Comentários (só se tiver dados)
        comment_graph = CommentGraph()
        if len(issues_df) > 0 or len(prs_df) > 0:
            comment_graph.build_from_data(issues_df, prs_df, issue_comments_df, pr_comments_df)
        self.graphs["comments"] = comment_graph
        
        # Grafo 2: Fechamento de Issues (só se tiver issues)
        issue_close_graph = IssueCloseGraph()
        if len(issues_df) > 0:
            issue_close_graph.build_from_data(issues_df)
        self.graphs["issue_closes"] = issue_close_graph
        
        # Grafo 3: Reviews e Merges (só se tiver PRs)
        review_graph = ReviewGraph()
        if len(prs_df) > 0:
            review_graph.build_from_data(prs_df, pr_reviews_df)
        self.graphs["reviews"] = review_graph
        
        # Grafo Integrado
        integrated_graph = IntegratedGraph()
        integrated_graph.build_from_data(issues_df, prs_df, issue_comments_df, pr_comments_df, pr_reviews_df)
        self.graphs["integrated"] = integrated_graph
        
        return self.graphs
    
    def export_all_graphs(self):
        """Exporta todos os grafos para arquivos"""
        print("Exportando grafos...")
        
        for name, graph in self.graphs.items():
            # Exporta para JSON
            json_path = os.path.join(self.output_dir, f"{name}_graph.json")
            graph.export_to_json(json_path)
            
            # Exporta para GEXF (formato Gephi)
            gexf_path = os.path.join(self.output_dir, f"{name}_graph.gexf")
            graph.export_to_gexf(gexf_path)
            
            print(f"  - {name}: {json_path}, {gexf_path}")
    
    def generate_report(self) -> Dict:
        """Gera relatório completo da análise"""
        print("Gerando relatório da análise...")
        
        report = {
            "repository": {
                "owner": os.getenv('REPO_OWNER', 'open-mmlab'),
                "name": os.getenv('REPO_NAME', 'mmdetection')
            },
            "data_summary": {},
            "graphs": {},
            "top_collaborators": {},
            "insights": []
        }
        
        # Resumo dos dados
        if self.data:
            report["data_summary"] = {
                "issues": len(self.data.get("issues", [])),
                "pull_requests": len(self.data.get("pull_requests", [])),
                "issue_comments": len(self.data.get("issue_comments", [])),
                "pr_comments": len(self.data.get("pr_comments", [])),
                "pr_reviews": len(self.data.get("pr_reviews", []))
            }
        
        # Estatísticas dos grafos
        if self.graphs:
            for name, graph in self.graphs.items():
                stats = graph.get_stats()
                report["graphs"][name] = stats
                
                # Top colaboradores para o grafo integrado
                if name == "integrated" and hasattr(graph, 'get_top_collaborators'):
                    report["top_collaborators"] = graph.get_top_collaborators(10)
                    
                    # Resumo de interações
                    if hasattr(graph, 'get_interaction_summary'):
                        report["interaction_summary"] = graph.get_interaction_summary()
        
        # Insights gerais
        if self.graphs and "integrated" in self.graphs:
            integrated = self.graphs["integrated"]
            stats = integrated.get_stats()
            
            report["insights"] = [
                f"O repositório possui {stats['nodes']} usuários únicos com interações",
                f"Total de {stats['edges']} conexões entre usuários",
                f"Peso total das interações: {stats['total_weight']}",
                f"Densidade do grafo: {stats['density']:.4f}",
                f"Grafo conectado: {'Sim' if stats['is_connected'] else 'Não'}"
            ]
            
            if report["top_collaborators"]:
                top_user = report["top_collaborators"][0]
                report["insights"].append(
                    f"Usuário mais central: {top_user['username']} "
                    f"(score: {top_user['centrality_score']:.4f})"
                )
        
        # Salva relatório
        report_path = os.path.join(self.output_dir, "analysis_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Relatório salvo em: {report_path}")
        return report
    
    def print_summary(self):
        """Imprime resumo da análise no console"""
        if not self.graphs:
            print("Nenhum grafo construído ainda.")
            return
        
        print("\n" + "="*60)
        print("RESUMO DA ANÁLISE DE GRAFOS DE COLABORAÇÃO")
        print("="*60)
        
        # Estatísticas por grafo
        for name, graph in self.graphs.items():
            stats = graph.get_stats()
            print(f"\n{stats['name']}:")
            print(f"  - Nós (usuários): {stats['nodes']}")
            print(f"  - Arestas (interações): {stats['edges']}")
            print(f"  - Peso total: {stats['total_weight']}")
            print(f"  - Densidade: {stats['density']:.4f}")
            print(f"  - Conectado: {'Sim' if stats['is_connected'] else 'Não'}")
        
        # Top colaboradores do grafo integrado
        if "integrated" in self.graphs:
            integrated = self.graphs["integrated"]
            top_collaborators = integrated.get_top_collaborators(5)
            
            print(f"\nTOP 5 COLABORADORES (por centralidade):")
            for i, user in enumerate(top_collaborators, 1):
                print(f"  {i}. {user['username']}")
                print(f"     - Score de centralidade: {user['centrality_score']:.4f}")
                print(f"     - Total de interações: {user['total_interactions']}")
                print(f"     - Comentários: {user['comments_made']}")
                print(f"     - Reviews: {user['reviews_given']}")
                print(f"     - Merges: {user['prs_merged']}")
        
        print("\n" + "="*60)

def main():
    """Função principal para executar toda a análise"""
    # Configuração
    REPO_OWNER = os.getenv('REPO_OWNER', 'open-mmlab')
    REPO_NAME = os.getenv('REPO_NAME', 'mmdetection')
    MAX_ISSUES = int(os.getenv('MAX_ISSUES', 500))
    MAX_PRS = int(os.getenv('MAX_PRS', 500))
    
    # Inicializa builder
    builder = GraphBuilder()
    
    # Opção 1: Extrair dados do GitHub (requer token)
    try:
        builder.extract_and_load_data(REPO_OWNER, REPO_NAME, MAX_ISSUES, MAX_PRS)
    except Exception as e:
        print(f"Erro ao extrair dados do GitHub: {e}")
        print("Tentando carregar dados de arquivos CSV existentes...")
        
        # Opção 2: Carregar dados de arquivos CSV
        try:
            builder.load_data_from_csv(REPO_NAME)
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            print("Execute primeiro a extração de dados ou forneça arquivos CSV válidos.")
            return
    
    # Constrói grafos
    try:
        builder.build_all_graphs()
        
        # Exporta resultados
        builder.export_all_graphs()
        
        # Gera relatório
        builder.generate_report()
        
        # Imprime resumo
        builder.print_summary()
        
        print(f"\nAnálise concluída! Resultados salvos em '{builder.output_dir}/'")
        
    except Exception as e:
        print(f"Erro durante a construção dos grafos: {e}")

if __name__ == "__main__":
    main()