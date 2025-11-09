"""
Visualizador de Análises de Grafos
Trabalho de Teoria dos Grafos - Etapa 3

Gera gráficos e visualizações das análises de centralidade e métricas de rede.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import Dict, List, Tuple, Optional
import json
import os

# Configuração para português
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

class GraphVisualizer:
    """
    Classe para visualização das análises de grafos.
    """
    
    def __init__(self, output_dir: str = "../output"):
        """
        Inicializa o visualizador.
        
        Args:
            output_dir: Diretório para salvar visualizações
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Paleta de cores profissional
        self.colors = {
            'primary': '#2E86AB',      # Azul principal
            'secondary': '#A23B72',    # Rosa escuro
            'accent': '#F18F01',       # Laranja
            'success': '#C73E1D',      # Vermelho
            'info': '#5D737E',         # Cinza azulado
            'light': '#E8F4F8',       # Azul claro
            'dark': '#1B1B1E'          # Preto suave
        }
    
    def plot_centrality_comparison(self, 
                                 centrality_data: Dict[str, Dict[str, float]], 
                                 user_mapping: Dict[int, str],
                                 top_n: int = 15,
                                 save_path: str = "centrality_comparison.png"):
        """
        Cria gráfico comparando diferentes métricas de centralidade.
        
        Args:
            centrality_data: Dados de centralidade por métrica
            user_mapping: Mapeamento ID -> username
            top_n: Número de usuários top a mostrar
            save_path: Caminho para salvar o gráfico
        """
        # Seleciona usuários com maior centralidade de grau
        degree_centrality = centrality_data.get('degree_centrality', {})
        top_users = sorted(degree_centrality.items(), 
                          key=lambda x: x[1], reverse=True)[:top_n]
        user_ids = [user_id for user_id, _ in top_users]
        usernames = [user_mapping.get(int(user_id), f"user_{user_id}") for user_id in user_ids]
        
        # Prepara dados para cada métrica
        metrics = {
            'Grau': centrality_data.get('degree_centrality', {}),
            'Intermediação': centrality_data.get('betweenness_centrality', {}),
            'Proximidade': centrality_data.get('closeness_centrality', {}),
            'PageRank': centrality_data.get('pagerank_centrality', {}),
            'Autovetor': centrality_data.get('eigenvector_centrality', {})
        }
        
        # Configuração do gráfico
        fig, ax = plt.subplots(figsize=(15, 10))
        
        # Largura das barras
        bar_width = 0.15
        r = np.arange(len(usernames))
        
        # Cores para cada métrica
        colors = [self.colors['primary'], self.colors['secondary'], 
                 self.colors['accent'], self.colors['success'], self.colors['info']]
        
        # Plota barras para cada métrica
        for i, (metric_name, metric_data) in enumerate(metrics.items()):
            values = [metric_data.get(str(user_id), 0) for user_id in user_ids]
            
            # Normaliza valores para melhor visualização
            if values and max(values) > 0:
                values = [v / max(values) for v in values]
            
            bars = ax.bar(r + i * bar_width, values, bar_width, 
                         label=metric_name, color=colors[i % len(colors)], alpha=0.8)
            
            # Adiciona valores nas barras (apenas os maiores)
            for j, (bar, value) in enumerate(zip(bars, values)):
                if value > 0.1:  # Só mostra valores maiores
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                           f'{value:.2f}', ha='center', va='bottom', fontsize=8)
        
        # Configurações do gráfico
        ax.set_xlabel('Usuários', fontweight='bold')
        ax.set_ylabel('Centralidade Normalizada', fontweight='bold')
        ax.set_title('Comparação de Métricas de Centralidade\n(Top 15 Usuários por Grau)', 
                     fontweight='bold', fontsize=14, pad=20)
        
        # Ajusta eixo X
        ax.set_xticks(r + bar_width * 2)
        ax.set_xticklabels([name[:15] + '...' if len(name) > 15 else name 
                           for name in usernames], rotation=45, ha='right')
        
        # Legenda e grid
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim(0, 1.1)
        
        # Layout e salvamento
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, save_path), 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"📊 Gráfico de centralidade salvo: {save_path}")
    
    def plot_network_metrics(self, 
                            network_metrics: Dict[str, float],
                            save_path: str = "network_metrics.png"):
        """
        Cria gráfico das métricas da rede.
        
        Args:
            network_metrics: Métricas da rede
            save_path: Caminho para salvar o gráfico
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Densidade da Rede
        density = network_metrics.get('density', 0)
        ax1.bar(['Densidade'], [density], color=self.colors['primary'], alpha=0.8)
        ax1.set_ylim(0, 1)
        ax1.set_ylabel('Valor')
        ax1.set_title('Densidade da Rede', fontweight='bold')
        ax1.text(0, density + 0.02, f'{density:.4f}', ha='center', fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # 2. Coeficiente de Clustering
        clustering = network_metrics.get('average_clustering', 0)
        ax2.bar(['Clustering Médio'], [clustering], color=self.colors['secondary'], alpha=0.8)
        ax2.set_ylim(0, 1)
        ax2.set_ylabel('Valor')
        ax2.set_title('Coeficiente de Clustering', fontweight='bold')
        ax2.text(0, clustering + 0.02, f'{clustering:.4f}', ha='center', fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 3. Assortatividade
        assortativity = network_metrics.get('assortativity', 0)
        color = self.colors['success'] if assortativity >= 0 else self.colors['accent']
        ax3.bar(['Assortatividade'], [assortativity], color=color, alpha=0.8)
        ax3.set_ylim(-1, 1)
        ax3.set_ylabel('Valor')
        ax3.set_title('Assortatividade da Rede', fontweight='bold')
        ax3.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax3.text(0, assortativity + (0.02 if assortativity >= 0 else -0.05), 
                f'{assortativity:.4f}', ha='center', fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Componentes e Métricas Gerais
        vertex_count = network_metrics.get('vertex_count', 0)
        edge_count = network_metrics.get('edge_count', 0)
        avg_degree = network_metrics.get('average_degree', 0)
        
        metrics = ['Vértices', 'Arestas', 'Grau Médio']
        values = [vertex_count, edge_count, avg_degree]
        colors_list = [self.colors['info'], self.colors['accent'], self.colors['primary']]
        
        bars = ax4.bar(metrics, values, color=colors_list, alpha=0.8)
        ax4.set_ylabel('Quantidade')
        ax4.set_title('Métricas Estruturais', fontweight='bold')
        
        # Adiciona valores nas barras
        for bar, value in zip(bars, values):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values) * 0.01,
                    f'{int(value)}', ha='center', va='bottom', fontweight='bold')
        
        ax4.grid(True, alpha=0.3, axis='y')
        
        # Layout e salvamento
        plt.suptitle('Análise Estrutural da Rede de Colaboração', 
                    fontweight='bold', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, save_path), 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"📊 Gráfico de métricas da rede salvo: {save_path}")
    
    def plot_degree_distribution(self, 
                                graph,
                                user_mapping: Dict[int, str],
                                save_path: str = "degree_distribution.png"):
        """
        Cria gráfico da distribuição de graus.
        
        Args:
            graph: Grafo para análise
            user_mapping: Mapeamento ID -> username  
            save_path: Caminho para salvar o gráfico
        """
        # Calcula graus
        degrees = []
        for vertex_id in range(graph.getVertexCount()):
            in_degree = graph.getVertexInDegree(vertex_id)
            out_degree = graph.getVertexOutDegree(vertex_id)
            total_degree = in_degree + out_degree
            degrees.append((vertex_id, in_degree, out_degree, total_degree))
        
        # Separa dados
        in_degrees = [d[1] for d in degrees]
        out_degrees = [d[2] for d in degrees]
        total_degrees = [d[3] for d in degrees]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        # 1. Histograma da distribuição
        ax1.hist(total_degrees, bins=20, alpha=0.7, color=self.colors['primary'], 
                edgecolor='black', label='Grau Total')
        ax1.hist(in_degrees, bins=20, alpha=0.5, color=self.colors['secondary'], 
                edgecolor='black', label='Grau de Entrada')
        ax1.hist(out_degrees, bins=20, alpha=0.5, color=self.colors['accent'], 
                edgecolor='black', label='Grau de Saída')
        
        ax1.set_xlabel('Grau')
        ax1.set_ylabel('Frequência')
        ax1.set_title('Distribuição de Graus', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Top usuários por grau
        top_users = sorted(degrees, key=lambda x: x[3], reverse=True)[:15]
        usernames = [user_mapping.get(user[0], f"user_{user[0]}")[:15] + 
                    ('...' if len(user_mapping.get(user[0], '')) > 15 else '') 
                    for user in top_users]
        user_degrees = [user[3] for user in top_users]
        
        bars = ax2.barh(range(len(usernames)), user_degrees, 
                       color=self.colors['primary'], alpha=0.8)
        ax2.set_yticks(range(len(usernames)))
        ax2.set_yticklabels(usernames)
        ax2.set_xlabel('Grau Total')
        ax2.set_title('Top 15 Usuários por Grau', fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')
        
        # Adiciona valores nas barras
        for i, (bar, degree) in enumerate(zip(bars, user_degrees)):
            ax2.text(bar.get_width() + max(user_degrees) * 0.01, bar.get_y() + bar.get_height()/2,
                    str(degree), va='center', fontweight='bold')
        
        ax2.invert_yaxis()  # Inverte para mostrar maior no topo
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, save_path), 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"📊 Gráfico de distribuição de graus salvo: {save_path}")
    
    def plot_community_analysis(self, 
                               community_metrics: Dict[str, float],
                               save_path: str = "community_analysis.png"):
        """
        Cria gráfico da análise de comunidades.
        
        Args:
            community_metrics: Métricas de comunidades
            save_path: Caminho para salvar o gráfico
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
        
        # 1. Modularidade
        modularity = community_metrics.get('modularity', 0)
        bridging_ties_ratio = community_metrics.get('bridging_ties_ratio', 0)
        
        metrics = ['Modularidade', 'Proporção de\nLigações Entre Grupos']
        values = [modularity, bridging_ties_ratio]
        colors_list = [self.colors['primary'], self.colors['secondary']]
        
        bars = ax1.bar(metrics, values, color=colors_list, alpha=0.8)
        ax1.set_ylabel('Valor')
        ax1.set_title('Métricas de Estrutura Comunitária', fontweight='bold')
        ax1.set_ylim(0, max(1, max(values) * 1.1))
        
        # Adiciona valores nas barras
        for bar, value in zip(bars, values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values) * 0.02,
                    f'{value:.4f}', ha='center', va='bottom', fontweight='bold')
        
        ax1.grid(True, alpha=0.3, axis='y')
        
        # 2. Interpretação da modularidade
        ax2.axis('off')
        
        # Texto explicativo baseado na modularidade
        if modularity > 0.3:
            interpretation = "ALTA\nEstrutura comunitária bem definida"
            color = self.colors['success']
        elif modularity > 0.1:
            interpretation = "MODERADA\nAlguma estrutura comunitária presente"  
            color = self.colors['accent']
        else:
            interpretation = "BAIXA\nEstrutura comunitária fraca"
            color = self.colors['info']
        
        ax2.text(0.5, 0.7, f'Modularidade: {modularity:.4f}', 
                ha='center', va='center', fontsize=16, fontweight='bold',
                transform=ax2.transAxes)
        
        ax2.text(0.5, 0.5, interpretation, 
                ha='center', va='center', fontsize=14, color=color,
                bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.2),
                transform=ax2.transAxes)
        
        if bridging_ties_ratio > 0:
            ax2.text(0.5, 0.3, 
                    f'Ligações entre grupos: {bridging_ties_ratio:.1%}',
                    ha='center', va='center', fontsize=12,
                    transform=ax2.transAxes)
        
        ax2.set_title('Interpretação da Análise Comunitária', 
                     fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, save_path), 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"📊 Gráfico de análise comunitária salvo: {save_path}")
    
    def create_summary_report(self, 
                             analysis_results: Dict,
                             user_mapping: Dict[int, str],
                             save_path: str = "analysis_summary.json"):
        """
        Cria relatório resumo da análise em JSON.
        
        Args:
            analysis_results: Resultados completos da análise
            user_mapping: Mapeamento ID -> username
            save_path: Caminho para salvar o relatório
        """
        # Converte IDs para usernames nos resultados de centralidade
        centrality_by_user = {}
        
        for metric, data in analysis_results.get('centrality', {}).items():
            centrality_by_user[metric] = {}
            for user_id, value in data.items():
                username = user_mapping.get(int(user_id), f"user_{user_id}")
                centrality_by_user[metric][username] = value
        
        # Encontra top usuários por métrica
        top_users_by_metric = {}
        for metric, data in centrality_by_user.items():
            sorted_users = sorted(data.items(), key=lambda x: x[1], reverse=True)
            top_users_by_metric[metric] = sorted_users[:10]
        
        # Monta relatório
        report = {
            "metadata": {
                "timestamp": "Análise gerada automaticamente",
                "total_users": len(user_mapping),
                "analysis_type": "Rede de Colaboração GitHub"
            },
            "network_structure": analysis_results.get('network_metrics', {}),
            "top_users_by_centrality": top_users_by_metric,
            "community_analysis": analysis_results.get('community_metrics', {}),
            "key_insights": self._generate_insights(analysis_results, user_mapping)
        }
        
        # Salva relatório
        report_path = os.path.join(self.output_dir, save_path)
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Relatório resumo salvo: {save_path}")
        return report
    
    def _generate_insights(self, analysis_results: Dict, user_mapping: Dict[int, str]) -> List[str]:
        """
        Gera insights automáticos da análise.
        
        Args:
            analysis_results: Resultados da análise
            user_mapping: Mapeamento ID -> username
            
        Returns:
            Lista de insights
        """
        insights = []
        
        # Métricas da rede
        network = analysis_results.get('network_metrics', {})
        density = network.get('density', 0)
        clustering = network.get('average_clustering', 0)
        assortativity = network.get('assortativity', 0)
        
        # Insights sobre densidade
        if density < 0.01:
            insights.append("Rede muito esparsa - poucas conexões entre desenvolvedores")
        elif density < 0.05:
            insights.append("Rede esparsa - colaboração concentrada em grupos específicos")
        else:
            insights.append("Rede densa - alta colaboração entre desenvolvedores")
        
        # Insights sobre clustering
        if clustering > 0.3:
            insights.append("Alto clustering - desenvolvedores formam grupos coesos")
        elif clustering > 0.1:
            insights.append("Clustering moderado - alguns grupos de colaboração identificados")
        else:
            insights.append("Baixo clustering - colaboração mais distribuída")
        
        # Insights sobre assortatividade
        if assortativity > 0.1:
            insights.append("Rede assortativa - desenvolvedores similares tendem a colaborar")
        elif assortativity < -0.1:
            insights.append("Rede disassortativa - desenvolvedores diferentes se conectam mais")
        else:
            insights.append("Assortatividade neutra - sem padrão específico de conexão")
        
        # Insights sobre centralidade
        centrality = analysis_results.get('centrality', {})
        degree_centrality = centrality.get('degree_centrality', {})
        
        if degree_centrality:
            top_user = max(degree_centrality.items(), key=lambda x: x[1])
            username = user_mapping.get(int(top_user[0]), f"user_{top_user[0]}")
            insights.append(f"Usuário mais conectado: {username} (grau: {top_user[1]:.3f})")
        
        # Insights sobre comunidades
        community = analysis_results.get('community_metrics', {})
        modularity = community.get('modularity', 0)
        
        if modularity > 0.3:
            insights.append("Estrutura comunitária forte - comunidades bem definidas")
        elif modularity > 0.1:
            insights.append("Estrutura comunitária moderada - alguns subgrupos identificados")
        else:
            insights.append("Estrutura comunitária fraca - colaboração mais uniforme")
        
        return insights