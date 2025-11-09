"""
Visualizador de Análises de Grafos
Trabalho de Teoria dos Grafos - Etapa 3

Gera gráficos e visualizações das análises de centralidade e métricas de rede.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import Dict, List, Tuple, Optional, Set
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
    
    def plot_directed_graph_structure(self, 
                                     graph,
                                     user_mapping: Dict[int, str],
                                     centrality_data: Dict[str, Dict[str, float]],
                                     save_path: str = "grafo_direcionado.png"):
        """
        Visualiza a estrutura do grafo direcionado.
        
        Args:
            graph: Grafo direcionado
            user_mapping: Mapeamento ID -> username
            centrality_data: Dados de centralidade
            save_path: Caminho para salvar
        """
        # Seleciona top 30 usuários para visualização (grafo completo seria muito poluído)
        degree_centrality = centrality_data.get('degree_centrality', {})
        top_users = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:30]
        top_user_ids = [int(user_id) for user_id, _ in top_users]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9))
        
        # 1. Grafo com layout circular
        positions = {}
        angle_step = 2 * 3.14159 / len(top_user_ids)
        
        for i, user_id in enumerate(top_user_ids):
            angle = i * angle_step
            radius = 3
            positions[user_id] = (radius * (angle / 6.28), radius * (angle / 6.28 + 1))
        
        # Desenha nós
        for user_id in top_user_ids:
            x, y = positions[user_id]
            centrality = degree_centrality.get(str(user_id), 0)
            
            # Tamanho proporcional à centralidade
            size = 100 + centrality * 2000
            
            # Cor baseada no PageRank
            pagerank = centrality_data.get('pagerank_centrality', {}).get(str(user_id), 0)
            color_intensity = min(1.0, pagerank * 10)  # Normaliza
            
            ax1.scatter(x, y, s=size, c=color_intensity, cmap='viridis', 
                       alpha=0.7, edgecolors='black', linewidth=1)
            
            # Label do usuário
            username = user_mapping.get(user_id, f"user_{user_id}")
            short_name = username[:8] + '...' if len(username) > 8 else username
            ax1.annotate(short_name, (x, y), xytext=(5, 5), textcoords='offset points',
                        fontsize=8, ha='left')
        
        # Desenha arestas direcionadas
        for source_id in top_user_ids:
            successors = graph.getSuccessors(source_id)
            for target_id in successors:
                if target_id in top_user_ids:
                    x1, y1 = positions[source_id]
                    x2, y2 = positions[target_id]
                    
                    # Peso da aresta
                    weight = graph.getEdgeWeight(source_id, target_id) if graph.hasEdge(source_id, target_id) else 1
                    line_width = max(0.5, weight / 3)  # Espessura baseada no peso
                    
                    # Seta direcionada
                    ax1.annotate('', xy=(x2, y2), xytext=(x1, y1),
                               arrowprops=dict(arrowstyle='->', lw=line_width, 
                                             color=self.colors['primary'], alpha=0.6))
        
        ax1.set_title('Rede de Colaboração Direcionada\n(Top 30 Usuários)', 
                     fontweight='bold', fontsize=14)
        ax1.set_xlabel('Posição X')
        ax1.set_ylabel('Posição Y')
        ax1.grid(True, alpha=0.3)
        
        # 2. Análise de graus de entrada vs saída
        in_degrees = []
        out_degrees = []
        usernames = []
        
        for user_id, _ in top_users[:15]:  # Top 15 para melhor visualização
            user_id_int = int(user_id)
            in_deg = graph.getVertexInDegree(user_id_int)
            out_deg = graph.getVertexOutDegree(user_id_int)
            
            in_degrees.append(in_deg)
            out_degrees.append(out_deg)
            username = user_mapping.get(user_id_int, f"user_{user_id}")
            usernames.append(username[:12] + '...' if len(username) > 12 else username)
        
        x = range(len(usernames))
        width = 0.35
        
        bars1 = ax2.bar([i - width/2 for i in x], in_degrees, width, 
                       label='Grau de Entrada', color=self.colors['secondary'], alpha=0.8)
        bars2 = ax2.bar([i + width/2 for i in x], out_degrees, width,
                       label='Grau de Saída', color=self.colors['primary'], alpha=0.8)
        
        ax2.set_xlabel('Usuários')
        ax2.set_ylabel('Grau')
        ax2.set_title('Graus de Entrada vs Saída\n(Top 15 Usuários)', fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(usernames, rotation=45, ha='right')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Adiciona valores nas barras
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                            f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, save_path), 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"📊 Gráfico do grafo direcionado salvo: {save_path}")
    
    def plot_community_detection_detailed(self,
                                        graph,
                                        analyzer,
                                        user_mapping: Dict[int, str],
                                        save_path: str = "deteccao_comunidades.png"):
        """
        Visualização detalhada da detecção de comunidades.
        
        Args:
            graph: Grafo para análise
            analyzer: Analisador com métodos de comunidade
            user_mapping: Mapeamento ID -> username
            save_path: Caminho para salvar
        """
        # Detecta comunidades
        communities = analyzer._detect_simple_communities()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Distribuição de tamanhos das comunidades
        community_sizes = [len(vertices) for vertices in communities.values()]
        
        ax1.hist(community_sizes, bins=20, color=self.colors['primary'], alpha=0.7, edgecolor='black')
        ax1.set_xlabel('Tamanho da Comunidade')
        ax1.set_ylabel('Frequência')
        ax1.set_title('Distribuição de Tamanhos das Comunidades', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Estatísticas
        if community_sizes:
            mean_size = sum(community_sizes) / len(community_sizes)
            max_size = max(community_sizes)
            ax1.axvline(mean_size, color='red', linestyle='--', 
                       label=f'Média: {mean_size:.1f}')
            ax1.legend()
        
        # 2. Top 10 maiores comunidades
        largest_communities = sorted(communities.items(), 
                                   key=lambda x: len(x[1]), reverse=True)[:10]
        
        comm_labels = [f'Com. {comm_id}' for comm_id, _ in largest_communities]
        comm_sizes = [len(vertices) for _, vertices in largest_communities]
        
        bars = ax2.bar(comm_labels, comm_sizes, color=self.colors['secondary'], alpha=0.8)
        ax2.set_xlabel('Comunidades')
        ax2.set_ylabel('Número de Usuários')
        ax2.set_title('Top 10 Maiores Comunidades', fontweight='bold')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Adiciona valores
        for bar, size in zip(bars, comm_sizes):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(size), ha='center', va='bottom', fontweight='bold')
        
        # 3. Densidade interna das comunidades
        densities = []
        comm_names = []
        
        for comm_id, vertices in largest_communities[:8]:  # Top 8 para visualização
            vertices_list = list(vertices)
            if len(vertices_list) > 1:
                # Conta arestas internas
                internal_edges = 0
                possible_edges = len(vertices_list) * (len(vertices_list) - 1)
                
                for v in vertices_list:
                    successors = graph.getSuccessors(v)
                    for neighbor in successors:
                        if neighbor in vertices:
                            internal_edges += 1
                
                density = internal_edges / possible_edges if possible_edges > 0 else 0
                densities.append(density)
                comm_names.append(f'C{comm_id}')
        
        if densities:
            bars3 = ax3.bar(comm_names, densities, color=self.colors['accent'], alpha=0.8)
            ax3.set_xlabel('Comunidades')
            ax3.set_ylabel('Densidade Interna')
            ax3.set_title('Densidade Interna das Comunidades', fontweight='bold')
            ax3.grid(True, alpha=0.3, axis='y')
            ax3.set_ylim(0, max(1, max(densities) * 1.1))
            
            # Adiciona valores
            for bar, density in zip(bars3, densities):
                ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{density:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # 4. Bridging ties - usuários que conectam comunidades
        bridging_users = self._find_bridging_users(graph, communities, user_mapping)
        
        if bridging_users:
            # Top 10 bridging users
            top_bridging = sorted(bridging_users.items(), 
                                key=lambda x: x[1], reverse=True)[:10]
            
            bridge_names = [user_mapping.get(user_id, f"user_{user_id}")[:10] + 
                           ('...' if len(user_mapping.get(user_id, '')) > 10 else '')
                           for user_id, _ in top_bridging]
            bridge_counts = [count for _, count in top_bridging]
            
            bars4 = ax4.barh(range(len(bridge_names)), bridge_counts, 
                           color=self.colors['success'], alpha=0.8)
            ax4.set_yticks(range(len(bridge_names)))
            ax4.set_yticklabels(bridge_names)
            ax4.set_xlabel('Conexões Entre Comunidades')
            ax4.set_title('Top 10 Usuários "Ponte"\n(Bridging Ties)', fontweight='bold')
            ax4.grid(True, alpha=0.3, axis='x')
            ax4.invert_yaxis()
            
            # Adiciona valores
            for i, (bar, count) in enumerate(zip(bars4, bridge_counts)):
                ax4.text(bar.get_width() + max(bridge_counts) * 0.01, bar.get_y() + bar.get_height()/2,
                        str(count), va='center', fontweight='bold')
        else:
            ax4.text(0.5, 0.5, 'Nenhum usuário ponte\nidentificado', 
                    ha='center', va='center', transform=ax4.transAxes,
                    fontsize=12, style='italic')
            ax4.set_title('Análise de Bridging Ties', fontweight='bold')
        
        plt.suptitle('Análise Detalhada de Comunidades', fontweight='bold', fontsize=16)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, save_path), 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"📊 Gráfico de detecção de comunidades salvo: {save_path}")
    
    def _find_bridging_users(self, graph, communities: Dict[int, set], 
                           user_mapping: Dict[int, str]) -> Dict[int, int]:
        """
        Encontra usuários que atuam como ponte entre comunidades.
        
        Args:
            graph: Grafo para análise
            communities: Comunidades detectadas
            user_mapping: Mapeamento de usuários
            
        Returns:
            Dicionário {user_id: num_bridging_connections}
        """
        # Mapeamento usuário -> comunidade
        user_to_community = {}
        for comm_id, users in communities.items():
            for user in users:
                user_to_community[user] = comm_id
        
        bridging_counts = {}
        
        for user_id in range(graph.getVertexCount()):
            if user_id not in user_to_community:
                continue
                
            user_community = user_to_community[user_id]
            bridging_connections = 0
            
            # Verifica sucessores (saídas)
            successors = graph.getSuccessors(user_id)
            for neighbor in successors:
                neighbor_community = user_to_community.get(neighbor, -1)
                if neighbor_community != user_community and neighbor_community != -1:
                    bridging_connections += 1
            
            # Verifica predecessores (entradas)
            for other_user in range(graph.getVertexCount()):
                if graph.hasEdge(other_user, user_id):
                    other_community = user_to_community.get(other_user, -1)
                    if other_community != user_community and other_community != -1:
                        bridging_connections += 1
            
            if bridging_connections > 0:
                bridging_counts[user_id] = bridging_connections
        
        return bridging_counts
    
    def plot_directed_flow_analysis(self,
                                   graph,
                                   user_mapping: Dict[int, str],
                                   centrality_data: Dict[str, Dict[str, float]],
                                   save_path: str = "analise_fluxo_direcionado.png"):
        """
        Analisa o fluxo direcionado da rede (who influences whom).
        
        Args:
            graph: Grafo direcionado
            user_mapping: Mapeamento ID -> username
            centrality_data: Dados de centralidade
            save_path: Caminho para salvar
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Análise de Influência vs Receptividade
        influence_scores = []  # Out-degree (quantos eles influenciam)
        receptivity_scores = []  # In-degree (quantos os influenciam)
        user_names = []
        
        degree_centrality = centrality_data.get('degree_centrality', {})
        top_users = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:20]
        
        for user_id, _ in top_users:
            user_id_int = int(user_id)
            out_degree = graph.getVertexOutDegree(user_id_int)
            in_degree = graph.getVertexInDegree(user_id_int)
            
            influence_scores.append(out_degree)
            receptivity_scores.append(in_degree)
            username = user_mapping.get(user_id_int, f"user_{user_id}")
            user_names.append(username[:10] + '...' if len(username) > 10 else username)
        
        # Scatter plot Influência vs Receptividade
        ax1.scatter(influence_scores, receptivity_scores, s=100, 
                   color=self.colors['primary'], alpha=0.7, edgecolors='black')
        
        # Adiciona labels dos usuários mais extremos
        for i, name in enumerate(user_names):
            if (influence_scores[i] > max(influence_scores) * 0.7 or 
                receptivity_scores[i] > max(receptivity_scores) * 0.7):
                ax1.annotate(name, (influence_scores[i], receptivity_scores[i]),
                           xytext=(5, 5), textcoords='offset points', fontsize=9)
        
        ax1.set_xlabel('Influência (Grau de Saída)')
        ax1.set_ylabel('Receptividade (Grau de Entrada)')
        ax1.set_title('Influência vs Receptividade', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Linha diagonal para comparação
        max_val = max(max(influence_scores) if influence_scores else 1, 
                     max(receptivity_scores) if receptivity_scores else 1)
        ax1.plot([0, max_val], [0, max_val], 'r--', alpha=0.5, label='Influência = Receptividade')
        ax1.legend()
        
        # 2. Razão Influência/Receptividade
        ratios = []
        ratio_names = []
        
        for i, name in enumerate(user_names):
            if receptivity_scores[i] > 0:  # Evita divisão por zero
                ratio = influence_scores[i] / receptivity_scores[i]
                if ratio > 0.1 and ratio < 10:  # Remove valores extremos
                    ratios.append(ratio)
                    ratio_names.append(name)
        
        if ratios:
            # Separa em influenciadores vs receptores
            influencers = [(name, ratio) for name, ratio in zip(ratio_names, ratios) if ratio > 1.2]
            receivers = [(name, ratio) for name, ratio in zip(ratio_names, ratios) if ratio < 0.8]
            
            if influencers:
                influencers.sort(key=lambda x: x[1], reverse=True)
                influencers = influencers[:8]  # Top 8
                
                names = [name for name, _ in influencers]
                vals = [ratio for _, ratio in influencers]
                
                bars = ax2.barh(range(len(names)), vals, color=self.colors['accent'], alpha=0.8)
                ax2.set_yticks(range(len(names)))
                ax2.set_yticklabels(names)
                ax2.set_xlabel('Razão Influência/Receptividade')
                ax2.set_title('Top Influenciadores\n(Razão > 1.2)', fontweight='bold')
                ax2.invert_yaxis()
                ax2.axvline(1, color='red', linestyle='--', alpha=0.7)
                ax2.grid(True, alpha=0.3, axis='x')
                
                # Adiciona valores
                for bar, val in zip(bars, vals):
                    ax2.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                            f'{val:.2f}', va='center', fontweight='bold')
        
        # 3. PageRank vs Betweenness (mostra diferentes tipos de importância)
        pagerank_values = []
        betweenness_values = []
        pr_bt_names = []
        
        pagerank_data = centrality_data.get('pagerank_centrality', {})
        betweenness_data = centrality_data.get('betweenness_centrality', {})
        
        for user_id, _ in top_users[:15]:
            pagerank_val = pagerank_data.get(str(user_id), 0)
            betweenness_val = betweenness_data.get(str(user_id), 0)
            
            pagerank_values.append(pagerank_val * 1000)  # Escala para visualização
            betweenness_values.append(betweenness_val * 1000)  # Escala para visualização
            
            username = user_mapping.get(int(user_id), f"user_{user_id}")
            pr_bt_names.append(username[:8] + '...' if len(username) > 8 else username)
        
        ax3.scatter(pagerank_values, betweenness_values, s=100,
                   color=self.colors['secondary'], alpha=0.7, edgecolors='black')
        
        # Labels para pontos interessantes
        for i, name in enumerate(pr_bt_names):
            if (pagerank_values[i] > max(pagerank_values) * 0.6 or 
                betweenness_values[i] > max(betweenness_values) * 0.6):
                ax3.annotate(name, (pagerank_values[i], betweenness_values[i]),
                           xytext=(5, 5), textcoords='offset points', fontsize=9)
        
        ax3.set_xlabel('PageRank (×1000)')
        ax3.set_ylabel('Betweenness Centrality (×1000)')
        ax3.set_title('PageRank vs Intermediação\n(Diferentes Tipos de Importância)', fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # 4. Reciprocidade de Conexões
        reciprocal_edges = 0
        total_directed_edges = graph.getEdgeCount()
        
        for u in range(graph.getVertexCount()):
            successors = graph.getSuccessors(u)
            for v in successors:
                if graph.hasEdge(v, u):  # Conexão recíproca
                    reciprocal_edges += 1
        
        reciprocal_edges = reciprocal_edges // 2  # Cada par é contado duas vezes
        reciprocity_rate = reciprocal_edges / total_directed_edges if total_directed_edges > 0 else 0
        
        # Gráfico de pizza
        labels = ['Conexões Recíprocas', 'Conexões Unidirecionais']
        sizes = [reciprocal_edges, total_directed_edges - reciprocal_edges]
        colors = [self.colors['primary'], self.colors['secondary']]
        
        ax4.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
        ax4.set_title(f'Reciprocidade da Rede\n({reciprocity_rate:.1%} das conexões são recíprocas)', 
                     fontweight='bold')
        
        plt.suptitle('Análise de Fluxo Direcionado da Rede', fontweight='bold', fontsize=16)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, save_path), 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"📊 Gráfico de análise de fluxo direcionado salvo: {save_path}")
    
    def plot_network_graph_manual(self,
                                  graph,
                                  user_mapping: Dict[int, str],
                                  centrality_data: Dict[str, Dict[str, float]],
                                  communities: Dict[int, Set[int]],
                                  save_path: str = "rede_grafo_manual.png"):
        """
        Desenha o grafo da rede manualmente usando apenas matplotlib.
        Implementa layout e desenho completamente do zero.
        
        Args:
            graph: Grafo para visualizar
            user_mapping: Mapeamento ID -> username
            centrality_data: Dados de centralidade
            communities: Comunidades detectadas
            save_path: Caminho para salvar
        """
        # Seleciona usuários mais importantes para visualização (grafo completo seria ilegível)
        degree_centrality = centrality_data.get('degree_centrality', {})
        top_users = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:50]
        selected_users = [int(user_id) for user_id, _ in top_users]
        
        print(f"   🎨 Desenhando grafo com {len(selected_users)} usuários principais...")
        
        # Gera posições usando algoritmo de força simples (implementado manualmente)
        positions = self._calculate_spring_layout(graph, selected_users)
        
        # Mapeia usuários para comunidades
        user_to_community = {}
        community_colors = {}
        color_palette = [self.colors['primary'], self.colors['secondary'], self.colors['accent'], 
                        self.colors['success'], self.colors['info'], '#FF6B6B', '#4ECDC4', '#45B7D1']
        
        for comm_id, users in communities.items():
            community_colors[comm_id] = color_palette[comm_id % len(color_palette)]
            for user in users:
                if user in selected_users:
                    user_to_community[user] = comm_id
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
        
        # 1. GRAFO POR CENTRALIDADE DE GRAU
        self._draw_graph_view(ax1, graph, positions, selected_users, user_mapping,
                             centrality_data.get('degree_centrality', {}),
                             "Grafo por Centralidade de Grau", "Degree Centrality")
        
        # 2. GRAFO POR BETWEENNESS CENTRALITY
        self._draw_graph_view(ax2, graph, positions, selected_users, user_mapping,
                             centrality_data.get('betweenness_centrality', {}),
                             "Grafo por Intermediação", "Betweenness")
        
        # 3. GRAFO POR PAGERANK
        self._draw_graph_view(ax3, graph, positions, selected_users, user_mapping,
                             centrality_data.get('pagerank_centrality', {}),
                             "Grafo por PageRank", "PageRank")
        
        # 4. GRAFO POR COMUNIDADES
        self._draw_community_graph(ax4, graph, positions, selected_users, user_mapping,
                                  user_to_community, community_colors)
        
        plt.suptitle('Visualização da Rede de Colaboração\n(Top 50 Usuários por Centralidade)', 
                     fontweight='bold', fontsize=18)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, save_path), 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"📊 Grafo de rede manual salvo: {save_path}")
    
    def _calculate_spring_layout(self, graph, selected_users: List[int], iterations: int = 50) -> Dict[int, Tuple[float, float]]:
        """
        Implementa algoritmo de layout spring (força) manualmente.
        Simula forças de atração e repulsão entre nós.
        
        Args:
            graph: Grafo para layoutar
            selected_users: Usuários selecionados
            iterations: Número de iterações
            
        Returns:
            Dicionário {user_id: (x, y)}
        """
        import random
        import math
        
        # Posições iniciais aleatórias
        positions = {}
        for user in selected_users:
            positions[user] = (random.uniform(-5, 5), random.uniform(-5, 5))
        
        # Parâmetros do algoritmo
        k = 2.0  # Distância ideal entre nós
        area = 100.0
        dt = 0.1  # Passo temporal
        
        for iteration in range(iterations):
            # Calcula forças
            forces = {user: [0.0, 0.0] for user in selected_users}
            
            # Força de repulsão (todos se repelem)
            for i, user1 in enumerate(selected_users):
                for j, user2 in enumerate(selected_users[i+1:], i+1):
                    x1, y1 = positions[user1]
                    x2, y2 = positions[user2]
                    
                    dx = x1 - x2
                    dy = y1 - y2
                    distance = max(0.01, (dx**2 + dy**2)**0.5)
                    
                    # Força de repulsão de Coulomb
                    force = k * k / distance
                    fx = force * dx / distance
                    fy = force * dy / distance
                    
                    forces[user1][0] += fx
                    forces[user1][1] += fy
                    forces[user2][0] -= fx
                    forces[user2][1] -= fy
            
            # Força de atração (nós conectados se atraem)
            for user1 in selected_users:
                successors = graph.getSuccessors(user1)
                for user2 in successors:
                    if user2 in selected_users:
                        x1, y1 = positions[user1]
                        x2, y2 = positions[user2]
                        
                        dx = x2 - x1
                        dy = y2 - y1
                        distance = max(0.01, (dx**2 + dy**2)**0.5)
                        
                        # Força de atração de mola
                        force = distance * distance / k
                        fx = force * dx / distance
                        fy = force * dy / distance
                        
                        forces[user1][0] += fx
                        forces[user1][1] += fy
                        forces[user2][0] -= fx
                        forces[user2][1] -= fy
            
            # Atualiza posições
            for user in selected_users:
                fx, fy = forces[user]
                
                # Limita força máxima
                force_mag = (fx**2 + fy**2)**0.5
                if force_mag > 1.0:
                    fx = fx / force_mag
                    fy = fy / force_mag
                
                # Atualiza posição
                x, y = positions[user]
                positions[user] = (x + fx * dt, y + fy * dt)
            
            # Resfriamento (reduz dt ao longo do tempo)
            dt *= 0.99
        
        return positions
    
    def _draw_graph_view(self, ax, graph, positions: Dict[int, Tuple[float, float]], 
                        selected_users: List[int], user_mapping: Dict[int, str],
                        centrality_values: Dict[str, float], title: str, metric_name: str):
        """
        Desenha uma visão do grafo colorida por uma métrica específica.
        
        Args:
            ax: Axes do matplotlib
            graph: Grafo a desenhar
            positions: Posições dos nós
            selected_users: Usuários selecionados
            user_mapping: Mapeamento ID -> nome
            centrality_values: Valores da métrica para colorir
            title: Título do gráfico
            metric_name: Nome da métrica
        """
        # Desenha arestas primeiro (para ficarem atrás dos nós)
        for user1 in selected_users:
            if user1 not in positions:
                continue
                
            successors = graph.getSuccessors(user1)
            for user2 in successors:
                if user2 in selected_users and user2 in positions:
                    x1, y1 = positions[user1]
                    x2, y2 = positions[user2]
                    
                    # Peso da aresta determina espessura
                    weight = graph.getEdgeWeight(user1, user2) if graph.hasEdge(user1, user2) else 1
                    line_width = max(0.2, min(2.0, weight / 3))
                    
                    ax.plot([x1, x2], [y1, y2], color='gray', alpha=0.4, linewidth=line_width)
        
        # Desenha nós
        for user in selected_users:
            if user not in positions:
                continue
                
            x, y = positions[user]
            centrality = centrality_values.get(str(user), 0)
            
            # Tamanho baseado na centralidade
            size = 50 + centrality * 800
            
            # Cor baseada na centralidade (normalizada)
            max_centrality = max(centrality_values.values()) if centrality_values else 1
            color_intensity = centrality / max_centrality if max_centrality > 0 else 0
            
            ax.scatter(x, y, s=size, c=color_intensity, cmap='viridis', 
                      alpha=0.8, edgecolors='black', linewidth=0.5)
            
            # Label para nós mais importantes
            if centrality > max_centrality * 0.5:
                username = user_mapping.get(user, f"user_{user}")
                short_name = username[:6] + '..' if len(username) > 6 else username
                ax.annotate(short_name, (x, y), xytext=(3, 3), textcoords='offset points',
                           fontsize=7, ha='left', weight='bold')
        
        ax.set_title(title, fontweight='bold', fontsize=12)
        ax.set_xlabel('Posição X')
        ax.set_ylabel('Posição Y')
        ax.grid(True, alpha=0.3)
        
        # Colorbar
        sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=0, vmax=max_centrality))
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, shrink=0.8)
        cbar.set_label(metric_name, fontsize=9)
    
    def _draw_community_graph(self, ax, graph, positions: Dict[int, Tuple[float, float]], 
                             selected_users: List[int], user_mapping: Dict[int, str],
                             user_to_community: Dict[int, int], community_colors: Dict[int, str]):
        """
        Desenha grafo colorido por comunidades.
        
        Args:
            ax: Axes do matplotlib
            graph: Grafo a desenhar
            positions: Posições dos nós
            selected_users: Usuários selecionados
            user_mapping: Mapeamento ID -> nome
            user_to_community: Mapeamento usuário -> comunidade
            community_colors: Cores das comunidades
        """
        # Desenha arestas coloridas por tipo (intra vs inter-comunidade)
        for user1 in selected_users:
            if user1 not in positions:
                continue
                
            successors = graph.getSuccessors(user1)
            for user2 in successors:
                if user2 in selected_users and user2 in positions:
                    x1, y1 = positions[user1]
                    x2, y2 = positions[user2]
                    
                    # Cor da aresta baseada se é intra ou inter-comunidade
                    comm1 = user_to_community.get(user1, -1)
                    comm2 = user_to_community.get(user2, -1)
                    
                    if comm1 == comm2 and comm1 != -1:
                        # Aresta interna da comunidade
                        color = community_colors.get(comm1, 'gray')
                        alpha = 0.6
                        linewidth = 1.0
                    else:
                        # Aresta entre comunidades (bridging tie)
                        color = 'red'
                        alpha = 0.8
                        linewidth = 1.5
                    
                    ax.plot([x1, x2], [y1, y2], color=color, alpha=alpha, linewidth=linewidth)
        
        # Desenha nós coloridos por comunidade
        for user in selected_users:
            if user not in positions:
                continue
                
            x, y = positions[user]
            community = user_to_community.get(user, -1)
            
            if community != -1:
                color = community_colors.get(community, 'gray')
                size = 100
                alpha = 0.8
            else:
                color = 'lightgray'
                size = 60
                alpha = 0.5
            
            ax.scatter(x, y, s=size, color=color, alpha=alpha, 
                      edgecolors='black', linewidth=0.5)
            
            # Labels para alguns nós
            if community != -1 and len(graph.getSuccessors(user)) > 2:
                username = user_mapping.get(user, f"user_{user}")
                short_name = username[:5] + '..' if len(username) > 5 else username
                ax.annotate(short_name, (x, y), xytext=(3, 3), textcoords='offset points',
                           fontsize=6, ha='left')
        
        ax.set_title('Grafo por Comunidades\n(Vermelho = Bridging Ties)', fontweight='bold', fontsize=12)
        ax.set_xlabel('Posição X')
        ax.set_ylabel('Posição Y')
        ax.grid(True, alpha=0.3)
        
        # Legenda das comunidades
        legend_elements = []
        for comm_id, color in list(community_colors.items())[:6]:  # Mostra só 6 para não poluir
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                            markerfacecolor=color, markersize=8, 
                                            label=f'Comunidade {comm_id}'))
        legend_elements.append(plt.Line2D([0], [0], color='red', linewidth=2, 
                                        label='Bridging Ties'))
        
        ax.legend(handles=legend_elements, loc='upper right', fontsize=8)
    
    def plot_bridging_ties_analysis(self,
                                   graph,
                                   analyzer,
                                   user_mapping: Dict[int, str],
                                   save_path: str = "bridging_ties_detalhado.png"):
        """
        Análise detalhada dos bridging ties (usuários ponte).
        
        Args:
            graph: Grafo para análise
            analyzer: Analisador com métodos de comunidade
            user_mapping: Mapeamento ID -> username
            save_path: Caminho para salvar
        """
        communities = analyzer._detect_simple_communities()
        bridging_users = self._find_bridging_users(graph, communities, user_mapping)
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Top Bridging Users
        if bridging_users:
            top_bridging = sorted(bridging_users.items(), key=lambda x: x[1], reverse=True)[:15]
            
            names = [user_mapping.get(user_id, f"user_{user_id}")[:12] + 
                    ('...' if len(user_mapping.get(user_id, '')) > 12 else '')
                    for user_id, _ in top_bridging]
            counts = [count for _, count in top_bridging]
            
            bars = ax1.barh(range(len(names)), counts, color=self.colors['primary'], alpha=0.8)
            ax1.set_yticks(range(len(names)))
            ax1.set_yticklabels(names)
            ax1.set_xlabel('Número de Conexões Entre Comunidades')
            ax1.set_title('Top 15 Usuários "Ponte"', fontweight='bold')
            ax1.invert_yaxis()
            ax1.grid(True, alpha=0.3, axis='x')
            
            # Adiciona valores
            for bar, count in zip(bars, counts):
                ax1.text(bar.get_width() + max(counts) * 0.01, bar.get_y() + bar.get_height()/2,
                        str(count), va='center', fontweight='bold')
        
        # 2. Distribuição de Bridging Ties por Comunidade
        community_bridging = {}
        
        for comm_id, users in communities.items():
            bridging_count = 0
            for user in users:
                bridging_count += bridging_users.get(user, 0)
            community_bridging[comm_id] = bridging_count
        
        # Top 10 comunidades com mais bridging ties
        top_comm_bridging = sorted(community_bridging.items(), 
                                 key=lambda x: x[1], reverse=True)[:10]
        
        if top_comm_bridging:
            comm_labels = [f'Comunidade {comm_id}' for comm_id, _ in top_comm_bridging]
            bridging_counts = [count for _, count in top_comm_bridging]
            
            bars2 = ax2.bar(range(len(comm_labels)), bridging_counts, 
                          color=self.colors['secondary'], alpha=0.8)
            ax2.set_xticks(range(len(comm_labels)))
            ax2.set_xticklabels([f'C{i}' for i in range(len(comm_labels))])
            ax2.set_ylabel('Total de Bridging Ties')
            ax2.set_title('Bridging Ties por Comunidade', fontweight='bold')
            ax2.grid(True, alpha=0.3, axis='y')
            
            # Adiciona valores
            for bar, count in zip(bars2, bridging_counts):
                if count > 0:
                    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(bridging_counts) * 0.01,
                            str(count), ha='center', va='bottom', fontweight='bold')
        
        # 3. Relação entre Centralidade e Bridging
        if bridging_users:
            from .GraphAnalyzer import GraphAnalyzer
            temp_analyzer = GraphAnalyzer(graph)
            degree_centrality = temp_analyzer.calculate_degree_centrality()
            betweenness_centrality = temp_analyzer.calculate_betweenness_centrality()
            
            bridging_values = []
            degree_values = []
            betweenness_values = []
            
            for user_id, bridging_count in bridging_users.items():
                if bridging_count > 0:
                    bridging_values.append(bridging_count)
                    degree_values.append(degree_centrality.get(user_id, 0))
                    betweenness_values.append(betweenness_centrality.get(user_id, 0) * 1000)
            
            if bridging_values:
                # Scatter plot Bridging vs Degree
                ax3.scatter(degree_values, bridging_values, s=60, alpha=0.7, 
                          color=self.colors['accent'], edgecolors='black', linewidth=0.5)
                ax3.set_xlabel('Centralidade de Grau')
                ax3.set_ylabel('Bridging Ties')
                ax3.set_title('Bridging Ties vs Centralidade de Grau', fontweight='bold')
                ax3.grid(True, alpha=0.3)
                
                # Scatter plot Bridging vs Betweenness
                ax4.scatter(betweenness_values, bridging_values, s=60, alpha=0.7,
                          color=self.colors['success'], edgecolors='black', linewidth=0.5)
                ax4.set_xlabel('Betweenness Centrality (×1000)')
                ax4.set_ylabel('Bridging Ties')
                ax4.set_title('Bridging Ties vs Intermediação', fontweight='bold')
                ax4.grid(True, alpha=0.3)
        
        plt.suptitle('Análise Detalhada de Bridging Ties', fontweight='bold', fontsize=16)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, save_path), 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"📊 Análise detalhada de bridging ties salva: {save_path}")
    
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