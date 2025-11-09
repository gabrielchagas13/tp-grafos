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
from datetime import datetime
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
    
    def create_complete_html_report(self, graphs: Dict[str, CollaborationGraph], save: bool = True):
        """Cria um relatório HTML completo com todos os grafos e interpretações"""
        
        if "integrated" not in graphs:
            print("Grafo integrado não encontrado")
            return
        
        integrated = graphs["integrated"]
        
        # Coleta dados para o relatório
        stats_data = []
        for name, graph in graphs.items():
            stats = graph.get_stats()
            stats_data.append(stats)
        
        # Top colaboradores
        top_collaborators = []
        if hasattr(integrated, 'get_top_collaborators'):
            top_collaborators = integrated.get_top_collaborators(10)
        
        # Resumo de interações
        interaction_summary = {}
        if hasattr(integrated, 'get_interaction_summary'):
            interaction_summary = integrated.get_interaction_summary()
        
        # HTML Template
        html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análise de Grafos de Colaboração - MMDetection</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        .header {{
            text-align: center;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .section {{
            margin: 30px 0;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 5px solid #007bff;
        }}
        .section h2 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            font-size: 1.8em;
        }}
        .graph-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .graph-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border: 2px solid #e9ecef;
            transition: transform 0.3s ease;
        }}
        .graph-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        .graph-title {{
            font-weight: bold;
            font-size: 1.3em;
            color: #2c3e50;
            margin-bottom: 15px;
            text-align: center;
            background: linear-gradient(45deg, #3498db, #2ecc71);
            color: white;
            padding: 10px;
            border-radius: 5px;
        }}
        .metric {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }}
        .metric:last-child {{
            border-bottom: none;
        }}
        .metric-label {{
            font-weight: 600;
            color: #34495e;
        }}
        .metric-value {{
            font-weight: bold;
            color: #2980b9;
        }}
        .interpretation {{
            background: #e8f4fd;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
            margin: 15px 0;
        }}
        .interpretation h3 {{
            color: #2980b9;
            margin-top: 0;
        }}
        .collaborators-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .collaborator-card {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            border: 1px solid #dee2e6;
        }}
        .collaborator-name {{
            font-weight: bold;
            font-size: 1.1em;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .interaction-types {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
        }}
        .interaction-badge {{
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }}
        .insights {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        .insights h3 {{
            margin-top: 0;
            font-size: 1.5em;
        }}
        .insights ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        .insights li {{
            padding: 8px 0;
            padding-left: 25px;
            position: relative;
        }}
        .insights li:before {{
            content: "🔍";
            position: absolute;
            left: 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            background: #2c3e50;
            color: white;
            border-radius: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🕸️ Análise de Grafos de Colaboração</h1>
            <p>Repositório: open-mmlab/mmdetection</p>
            <p>Trabalho de Teoria dos Grafos - Etapa 1</p>
        </div>

        <div class="section">
            <h2>📊 Visão Geral dos Grafos</h2>
            <div class="graph-container">"""

        # Adiciona cards para cada grafo
        for stats in stats_data:
            html_content += f"""
                <div class="graph-card">
                    <div class="graph-title">{stats['name']}</div>
                    <div class="metric">
                        <span class="metric-label">Usuários (Nós):</span>
                        <span class="metric-value">{stats['nodes']}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Conexões (Arestas):</span>
                        <span class="metric-value">{stats['edges']}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Peso Total:</span>
                        <span class="metric-value">{stats['total_weight']}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Densidade:</span>
                        <span class="metric-value">{stats['density']:.4f}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Conectado:</span>
                        <span class="metric-value">{'✅ Sim' if stats['is_connected'] else '❌ Não'}</span>
                    </div>
                </div>"""

        html_content += """
            </div>
        </div>

        <div class="section">
            <h2>🎯 Interpretação dos Grafos</h2>
            
            <div class="interpretation">
                <h3>🗨️ Grafo de Comentários</h3>
                <p><strong>O que representa:</strong> Interações através de comentários em issues e pull requests.</p>
                <p><strong>Peso das arestas:</strong> 2 para comentários em PRs, 3 para comentários em issues.</p>
                <p><strong>Interpretação:</strong> Usuários com alto out-degree são comentaristas ativos. Usuários com alto in-degree são autores que geram discussão.</p>
            </div>

            <div class="interpretation">
                <h3>🔐 Grafo de Fechamento de Issues</h3>
                <p><strong>O que representa:</strong> Relação entre quem abre e quem fecha issues.</p>
                <p><strong>Peso das arestas:</strong> 3 para cada fechamento de issue.</p>
                <p><strong>Interpretação:</strong> Usuários com alto out-degree são solucionadores de problemas (mantenedores). Alto in-degree indica autores de issues que são resolvidas.</p>
            </div>

            <div class="interpretation">
                <h3>⭐ Grafo de Reviews e Merges</h3>
                <p><strong>O que representa:</strong> Interações através de code reviews, aprovações e merges.</p>
                <p><strong>Peso das arestas:</strong> 4 para reviews, 5 para merges.</p>
                <p><strong>Interpretação:</strong> Representa o núcleo técnico do projeto. Alto out-degree indica reviewers experientes e mantenedores.</p>
            </div>

            <div class="interpretation">
                <h3>🌐 Grafo Integrado</h3>
                <p><strong>O que representa:</strong> Combinação ponderada de todas as interações.</p>
                <p><strong>Peso das arestas:</strong> Soma ponderada de todos os tipos de interação.</p>
                <p><strong>Interpretação:</strong> Visão holística da rede de colaboração, identificando os usuários mais influentes e centrais.</p>
            </div>
        </div>

        <div class="section">
            <h2>🏆 Top 10 Colaboradores</h2>"""

        if top_collaborators:
            html_content += '<div class="collaborators-grid">'
            for i, collab in enumerate(top_collaborators, 1):
                html_content += f"""
                <div class="collaborator-card">
                    <div class="collaborator-name">#{i} {collab['username']}</div>
                    <div class="metric">
                        <span class="metric-label">Score de Centralidade:</span>
                        <span class="metric-value">{collab['centrality_score']:.4f}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Total de Interações:</span>
                        <span class="metric-value">{collab['total_interactions']}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Comentários:</span>
                        <span class="metric-value">{collab['comments_made']}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Reviews:</span>
                        <span class="metric-value">{collab['reviews_given']}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Merges:</span>
                        <span class="metric-value">{collab['prs_merged']}</span>
                    </div>
                </div>"""
            html_content += '</div>'

        html_content += """
        </div>

        <div class="section">
            <h2>🎨 Tipos de Interação</h2>"""

        if interaction_summary:
            html_content += '<div class="interaction-types">'
            for interaction_type, count in interaction_summary.items():
                html_content += f'<div class="interaction-badge">{interaction_type}: {count}</div>'
            html_content += '</div>'

        # Calcula algumas estatísticas interessantes
        total_nodes = sum(stats['nodes'] for stats in stats_data)
        total_edges = sum(stats['edges'] for stats in stats_data)
        total_weight = sum(stats['total_weight'] for stats in stats_data)

        html_content += f"""
        </div>

        <div class="section">
            <h2>🔍 Insights e Análise</h2>
            
            <div class="insights">
                <h3>Principais Descobertas</h3>
                <ul>
                    <li>O repositório possui <strong>{integrated.get_stats()['nodes']}</strong> usuários únicos com interações documentadas</li>
                    <li>Foram mapeadas <strong>{integrated.get_stats()['edges']}</strong> conexões diretas entre colaboradores</li>
                    <li>O peso total das interações é <strong>{integrated.get_stats()['total_weight']}</strong>, indicando alta atividade</li>
                    <li>A densidade do grafo é <strong>{integrated.get_stats()['density']:.4f}</strong>, mostrando {"uma rede bem conectada" if integrated.get_stats()['density'] > 0.1 else "uma rede com conexões esparsas"}</li>"""

        if top_collaborators:
            top_user = top_collaborators[0]
            html_content += f"""
                    <li>O usuário mais central é <strong>{top_user['username']}</strong> com score de centralidade <strong>{top_user['centrality_score']:.4f}</strong></li>"""

        html_content += """
                    <li>O grafo é {"fracamente conectado" if integrated.get_stats()['is_connected'] else "desconectado"}, indicando {"fluxo de informação" if integrated.get_stats()['is_connected'] else "grupos isolados"}</li>
                </ul>
            </div>

            <div class="interpretation">
                <h3>📈 Métricas de Centralidade</h3>
                <p><strong>Centralidade de Grau:</strong> Mede quantas conexões diretas um usuário possui. Alto valor indica usuários muito ativos.</p>
                <p><strong>Centralidade de Proximidade:</strong> Mede quão próximo um usuário está dos outros. Alto valor indica usuários que podem influenciar rapidamente a rede.</p>
                <p><strong>Centralidade de Intermediação:</strong> Mede quantas vezes um usuário aparece no caminho mais curto entre outros. Alto valor indica "pontes" na rede.</p>
                <p><strong>PageRank:</strong> Mede a importância baseada na qualidade das conexões. Alto valor indica usuários influentes.</p>
            </div>

            <div class="interpretation">
                <h3>🎯 Padrões Identificados</h3>
                <p><strong>Colaboradores Core:</strong> Usuários com alta centralidade em todos os grafos - são os mantenedores principais.</p>
                <p><strong>Especialistas Técnicos:</strong> Alta centralidade no grafo de reviews - focam na qualidade do código.</p>
                <p><strong>Facilitadores de Discussão:</strong> Alta centralidade no grafo de comentários - promovem comunicação.</p>
                <p><strong>Solucionadores:</strong> Alta centralidade no grafo de fechamento de issues - resolvem problemas ativamente.</p>
            </div>
        </div>

        <div class="section">
            <h2>📋 Metodologia</h2>
            <div class="interpretation">
                <h3>🔬 Como foi feita a análise</h3>
                <p><strong>1. Extração de Dados:</strong> Utilizamos a API REST do GitHub para coletar dados de issues, pull requests, comentários e reviews.</p>
                <p><strong>2. Modelagem:</strong> Cada usuário foi representado como um nó, e cada interação como uma aresta direcionada com peso específico.</p>
                <p><strong>3. Pesos:</strong> Comentários em PRs (2), comentários em issues (3), reviews (4), merges (5), fechamentos (3).</p>
                <p><strong>4. Análise:</strong> Aplicamos algoritmos de teoria dos grafos (NetworkX) para calcular métricas de centralidade.</p>
                <p><strong>5. Visualização:</strong> Criamos múltiplas perspectivas dos dados para análise holística.</p>
            </div>
        </div>

        <div class="footer">
            <p>📊 Análise gerada automaticamente em {datetime.now().strftime("%d/%m/%Y às %H:%M")}</p>
            <p>🔧 Tecnologias: Python, NetworkX, Plotly, GitHub API</p>
            <p>🎓 Trabalho de Teoria dos Grafos - Universidade</p>
        </div>
    </div>
</body>
</html>"""

        # Salva o arquivo
        if save:
            filepath = os.path.join(self.output_dir, "relatorio_completo.html")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Relatório HTML completo salvo: {filepath}")
            
            return filepath

def main():
    """Função de exemplo para usar o visualizador"""
    visualizer = GraphVisualizer()
    print("Visualizador criado. Use com grafos construídos pelo GraphBuilder.")

if __name__ == "__main__":
    main()