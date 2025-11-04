"""
Graph Visualizer
Módulo para visualização dos grafos de colaboração
"""

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Tuple
import os
from src.graph_models import CollaborationGraph

class GraphVisualizer:
    """Classe para visualização dos grafos de colaboração"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Configurações de estilo
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def plot_graph_basic(self, graph: CollaborationGraph, 
                        figsize: Tuple[int, int] = (12, 8),
                        save: bool = True) -> None:
        """Plota visualização básica do grafo usando NetworkX e Matplotlib"""
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Filtra nós com mais conexões para melhor visualização
        degrees = dict(graph.graph.degree())
        top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:50]
        subgraph = graph.graph.subgraph([node for node, _ in top_nodes])
        
        # Layout do grafo
        pos = nx.spring_layout(subgraph, k=1, iterations=50)
        
        # Tamanho dos nós baseado no grau
        node_sizes = [degrees[node] * 20 for node in subgraph.nodes()]
        
        # Cor dos nós baseada na centralidade
        centralities = nx.degree_centrality(subgraph)
        node_colors = [centralities[node] for node in subgraph.nodes()]
        
        # Desenha o grafo
        nx.draw_networkx_nodes(subgraph, pos, 
                              node_size=node_sizes,
                              node_color=node_colors,
                              cmap=plt.cm.viridis,
                              alpha=0.7, ax=ax)
        
        nx.draw_networkx_edges(subgraph, pos, 
                              alpha=0.3, 
                              edge_color='gray',
                              width=0.5, ax=ax)
        
        # Labels apenas para os top 10 nós
        top_10_nodes = dict(top_nodes[:10])
        labels = {node: node for node in top_10_nodes.keys() if node in subgraph.nodes()}
        nx.draw_networkx_labels(subgraph, pos, labels, 
                               font_size=8, font_weight='bold', ax=ax)
        
        ax.set_title(f"Grafo de {graph.name} - Top 50 Nós", fontsize=16, fontweight='bold')
        ax.axis('off')
        
        if save:
            filename = f"{graph.name.lower().replace(' ', '_')}_basic.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Gráfico salvo: {filepath}")
        
        plt.show()
    
    def plot_interactive_graph(self, graph: CollaborationGraph, save: bool = True) -> None:
        """Cria visualização interativa do grafo usando Plotly"""
        
        # Filtra top 30 nós para performance
        degrees = dict(graph.graph.degree())
        top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:30]
        subgraph = graph.graph.subgraph([node for node, _ in top_nodes])
        
        # Layout do grafo
        pos = nx.spring_layout(subgraph, k=2, iterations=50)
        
        # Prepara dados para Plotly
        edge_x = []
        edge_y = []
        for edge in subgraph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        # Trace das arestas
        edge_trace = go.Scatter(x=edge_x, y=edge_y,
                               line=dict(width=0.5, color='#888'),
                               hoverinfo='none',
                               mode='lines')
        
        # Prepara dados dos nós
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        node_color = []
        
        for node in subgraph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            # Informações do nó
            degree = degrees[node]
            node_info = graph.nodes.get(node)
            if node_info:
                centrality = node_info.metrics.get('centrality_score', 0)
                total_interactions = node_info.metrics.get('total_interactions', 0)
                
                text = f"{node}<br>Grau: {degree}<br>Centralidade: {centrality:.3f}<br>Interações: {total_interactions}"
                node_text.append(text)
                node_size.append(max(10, degree * 2))
                node_color.append(centrality)
            else:
                node_text.append(f"{node}<br>Grau: {degree}")
                node_size.append(max(10, degree * 2))
                node_color.append(0)
        
        # Trace dos nós
        node_trace = go.Scatter(x=node_x, y=node_y,
                               mode='markers+text',
                               hoverinfo='text',
                               text=[node for node in subgraph.nodes()],
                               textposition="middle center",
                               hovertext=node_text,
                               marker=dict(size=node_size,
                                          color=node_color,
                                          colorscale='Viridis',
                                          showscale=True,
                                          colorbar=dict(title="Centralidade"),
                                          line=dict(width=1, color='#000')))
        
        # Cria figura
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title=f'Grafo Interativo de {graph.name}',
                           titlefont_size=16,
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           annotations=[ dict(
                               text="Tamanho do nó = grau, Cor = centralidade",
                               showarrow=False,
                               xref="paper", yref="paper",
                               x=0.005, y=-0.002,
                               xanchor="left", yanchor="bottom",
                               font=dict(color="#888", size=12)
                           )],
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
        
        if save:
            filename = f"{graph.name.lower().replace(' ', '_')}_interactive.html"
            filepath = os.path.join(self.output_dir, filename)
            fig.write_html(filepath)
            print(f"Gráfico interativo salvo: {filepath}")
        
        fig.show()
    
    def plot_centrality_comparison(self, graphs: Dict[str, CollaborationGraph], 
                                  save: bool = True) -> None:
        """Compara métricas de centralidade entre diferentes grafos"""
        
        # Coleta dados de centralidade
        data = []
        for graph_name, graph in graphs.items():
            for username, node in graph.nodes.items():
                metrics = node.metrics
                data.append({
                    'graph': graph_name,
                    'username': username,
                    'degree_centrality': metrics.get('in_degree_centrality', 0) + 
                                       metrics.get('out_degree_centrality', 0),
                    'closeness_centrality': metrics.get('closeness_centrality', 0),
                    'betweenness_centrality': metrics.get('betweenness_centrality', 0),
                    'pagerank': metrics.get('pagerank', 0),
                    'total_interactions': metrics.get('total_interactions', 0)
                })
        
        df = pd.DataFrame(data)
        
        # Cria subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Comparação de Métricas de Centralidade', fontsize=16, fontweight='bold')
        
        # Plot 1: Degree Centrality
        sns.boxplot(data=df, x='graph', y='degree_centrality', ax=axes[0,0])
        axes[0,0].set_title('Centralidade de Grau')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # Plot 2: Closeness Centrality
        sns.boxplot(data=df, x='graph', y='closeness_centrality', ax=axes[0,1])
        axes[0,1].set_title('Centralidade de Proximidade')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # Plot 3: Betweenness Centrality
        sns.boxplot(data=df, x='graph', y='betweenness_centrality', ax=axes[1,0])
        axes[1,0].set_title('Centralidade de Intermediação')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # Plot 4: PageRank
        sns.boxplot(data=df, x='graph', y='pagerank', ax=axes[1,1])
        axes[1,1].set_title('PageRank')
        axes[1,1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save:
            filepath = os.path.join(self.output_dir, "centrality_comparison.png")
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Comparação de centralidade salva: {filepath}")
        
        plt.show()
    
    def plot_graph_metrics(self, graphs: Dict[str, CollaborationGraph], 
                          save: bool = True) -> None:
        """Plota métricas básicas dos grafos"""
        
        # Coleta estatísticas
        stats_data = []
        for name, graph in graphs.items():
            stats = graph.get_stats()
            stats_data.append({
                'Grafo': name,
                'Nós': stats['nodes'],
                'Arestas': stats['edges'],
                'Peso Total': stats['total_weight'],
                'Densidade': stats['density']
            })
        
        df_stats = pd.DataFrame(stats_data)
        
        # Cria subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Métricas dos Grafos de Colaboração', fontsize=16, fontweight='bold')
        
        # Plot 1: Número de nós
        sns.barplot(data=df_stats, x='Grafo', y='Nós', ax=axes[0,0], palette='viridis')
        axes[0,0].set_title('Número de Usuários')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # Plot 2: Número de arestas
        sns.barplot(data=df_stats, x='Grafo', y='Arestas', ax=axes[0,1], palette='plasma')
        axes[0,1].set_title('Número de Conexões')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # Plot 3: Peso total
        sns.barplot(data=df_stats, x='Grafo', y='Peso Total', ax=axes[1,0], palette='inferno')
        axes[1,0].set_title('Peso Total das Interações')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # Plot 4: Densidade
        sns.barplot(data=df_stats, x='Grafo', y='Densidade', ax=axes[1,1], palette='cividis')
        axes[1,1].set_title('Densidade do Grafo')
        axes[1,1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save:
            filepath = os.path.join(self.output_dir, "graph_metrics.png")
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Métricas dos grafos salvas: {filepath}")
        
        plt.show()
    
    def plot_top_collaborators(self, integrated_graph: CollaborationGraph, 
                              n: int = 15, save: bool = True) -> None:
        """Plota os top colaboradores do grafo integrado"""
        
        if not hasattr(integrated_graph, 'get_top_collaborators'):
            print("Grafo não possui método get_top_collaborators")
            return
        
        top_users = integrated_graph.get_top_collaborators(n)
        
        # Prepara dados
        usernames = [user['username'] for user in top_users]
        centrality_scores = [user['centrality_score'] for user in top_users]
        total_interactions = [user['total_interactions'] for user in top_users]
        
        # Cria subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
        
        # Plot 1: Score de centralidade
        bars1 = ax1.barh(range(len(usernames)), centrality_scores, color='skyblue')
        ax1.set_yticks(range(len(usernames)))
        ax1.set_yticklabels(usernames)
        ax1.set_xlabel('Score de Centralidade')
        ax1.set_title(f'Top {n} Colaboradores por Centralidade')
        ax1.invert_yaxis()
        
        # Adiciona valores nas barras
        for i, v in enumerate(centrality_scores):
            ax1.text(v + 0.001, i, f'{v:.3f}', va='center', fontsize=9)
        
        # Plot 2: Total de interações
        bars2 = ax2.barh(range(len(usernames)), total_interactions, color='lightcoral')
        ax2.set_yticks(range(len(usernames)))
        ax2.set_yticklabels(usernames)
        ax2.set_xlabel('Total de Interações')
        ax2.set_title(f'Top {n} Colaboradores por Interações')
        ax2.invert_yaxis()
        
        # Adiciona valores nas barras
        for i, v in enumerate(total_interactions):
            ax2.text(v + max(total_interactions)*0.01, i, str(v), va='center', fontsize=9)
        
        plt.tight_layout()
        
        if save:
            filepath = os.path.join(self.output_dir, "top_collaborators.png")
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Top colaboradores salvos: {filepath}")
        
        plt.show()
    
    def create_dashboard(self, graphs: Dict[str, CollaborationGraph], save: bool = True):
        """Cria um dashboard interativo com todas as visualizações"""
        
        if "integrated" not in graphs:
            print("Grafo integrado não encontrado para criar dashboard")
            return
        
        integrated = graphs["integrated"]
        
        # Dados para o dashboard
        stats_data = []
        for name, graph in graphs.items():
            stats = graph.get_stats()
            stats_data.append(stats)
        
        # Cria subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Métricas dos Grafos', 'Top Colaboradores', 
                           'Distribuição de Centralidade', 'Tipos de Interação'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "histogram"}, {"type": "pie"}]]
        )
        
        # Plot 1: Métricas dos grafos
        graph_names = [stats['name'] for stats in stats_data]
        nodes_count = [stats['nodes'] for stats in stats_data]
        edges_count = [stats['edges'] for stats in stats_data]
        
        fig.add_trace(go.Bar(x=graph_names, y=nodes_count, name='Nós', 
                            marker_color='lightblue'), row=1, col=1)
        
        # Plot 2: Top colaboradores
        if hasattr(integrated, 'get_top_collaborators'):
            top_users = integrated.get_top_collaborators(10)
            usernames = [user['username'][:15] for user in top_users]  # Trunca nomes longos
            scores = [user['centrality_score'] for user in top_users]
            
            fig.add_trace(go.Bar(x=usernames, y=scores, name='Centralidade',
                                marker_color='lightcoral'), row=1, col=2)
        
        # Plot 3: Distribuição de centralidade
        centrality_scores = [node.metrics.get('centrality_score', 0) 
                           for node in integrated.nodes.values()]
        
        fig.add_trace(go.Histogram(x=centrality_scores, name='Distribuição',
                                  marker_color='lightgreen'), row=2, col=1)
        
        # Plot 4: Tipos de interação
        if hasattr(integrated, 'get_interaction_summary'):
            interaction_summary = integrated.get_interaction_summary()
            labels = list(interaction_summary.keys())
            values = list(interaction_summary.values())
            
            fig.add_trace(go.Pie(labels=labels, values=values, name="Interações"),
                         row=2, col=2)
        
        # Atualiza layout
        fig.update_layout(
            title_text="Dashboard de Análise de Colaboração",
            title_x=0.5,
            showlegend=False,
            height=800
        )
        
        if save:
            filepath = os.path.join(self.output_dir, "dashboard.html")
            fig.write_html(filepath)
            print(f"Dashboard salvo: {filepath}")
        
        fig.show()

def main():
    """Função de exemplo para usar o visualizador"""
    visualizer = GraphVisualizer()
    print("Visualizador criado. Use com grafos construídos pelo GraphBuilder.")

if __name__ == "__main__":
    main()