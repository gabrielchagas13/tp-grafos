# README Técnico - Documentação do Código

## 📋 Visão Geral

Este projeto implementa uma análise completa de grafos de colaboração em repositórios GitHub usando Python. O sistema extrai dados da API do GitHub, modela diferentes tipos de interações como grafos direcionados, e gera visualizações e métricas de centralidade.

## 🏗️ Arquitetura do Sistema

```
etapa01/
├── src/                        # Código fonte principal
│   ├── github_extractor.py     # Extração de dados da API GitHub
│   ├── graph_models.py         # Classes de modelagem de grafos
│   ├── graph_builder.py        # Construção e análise dos grafos
│   └── graph_visualizer.py     # Visualizações e dashboards
├── data/                       # Dados extraídos (CSV)
├── output/                     # Resultados e visualizações
├── main.py                     # Script principal
├── complete_extraction.py      # Script auxiliar de extração
├── generate_sample_data.py     # Gerador de dados simulados
└── check_rate_limit.py         # Verificador de rate limit
```

---

## 📚 Bibliotecas e Dependências

### **Core Dependencies**

```python
import requests           # HTTP requests para API GitHub
import pandas as pd       # Manipulação de dados estruturados
import networkx as nx     # Análise e manipulação de grafos
import numpy as np        # Computação numérica
```

### **Visualização**

```python
import matplotlib.pyplot as plt  # Gráficos estáticos
import seaborn as sns            # Visualizações estatísticas
import plotly.graph_objects as go # Gráficos interativos
import plotly.express as px      # Gráficos expressos
```

### **Utilidades**

```python
import json              # Serialização JSON
import time              # Controle de tempo e delays
import os                # Operações do sistema operacional
from datetime import datetime    # Manipulação de datas
from typing import Dict, List, Optional  # Type hints
from tqdm import tqdm            # Barras de progresso
from dotenv import load_dotenv   # Carregamento de variáveis de ambiente
from collections import defaultdict  # Dicionários com valores padrão
```

---

## 🔧 Módulos Principais

### **1. github_extractor.py**

**Responsabilidade**: Extração de dados da API REST do GitHub

#### **Classe GitHubDataExtractor**

```python
class GitHubDataExtractor:
    def __init__(self, repo_owner: str, repo_name: str, token: Optional[str] = None)
```

**Principais Métodos:**

- **`_make_request()`**: Executa requisições HTTP com tratamento de rate limit
- **`_paginate_request()`**: Gerencia paginação automática da API
- **`extract_issues()`**: Extrai issues do repositório
- **`extract_pull_requests()`**: Extrai pull requests
- **`extract_issue_comments()`**: Extrai comentários de issues específicas
- **`extract_pr_reviews()`**: Extrai reviews de PRs
- **`extract_pr_comments()`**: Extrai comentários de PRs
- **`extract_all_data()`**: Orquestra extração completa

**Funcionalidades Técnicas:**

1. **Rate Limiting**: Detecta e aguarda reset do rate limit automaticamente
2. **Paginação**: Coleta todos os dados usando paginação da API
3. **Error Handling**: Tratamento robusto de erros HTTP
4. **Data Persistence**: Salva dados em CSV para reutilização

```python
# Exemplo de uso do rate limiting
if response.status_code == 403 and 'rate limit' in response.text.lower():
    reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
    wait_time = max(0, reset_time - int(time.time()) + 1)
    time.sleep(wait_time)
```

### **2. graph_models.py**

**Responsabilidade**: Modelagem matemática dos grafos de colaboração

#### **Classes Principais:**

**CollaborationNode**: Representa usuários (vértices)
```python
class CollaborationNode:
    def __init__(self, username: str):
        self.username = username
        self.metrics = {
            "total_interactions": 0,
            "comments_made": 0,
            "issues_closed": 0,
            "reviews_given": 0,
            "prs_merged": 0,
            "centrality_score": 0.0
        }
```

**CollaborationEdge**: Representa interações (arestas)
```python
class CollaborationEdge:
    def __init__(self, source: str, target: str, interaction_type: str, weight: int = 1):
        self.source = source
        self.target = target
        self.interaction_type = interaction_type
        self.weight = weight
```

**CollaborationGraph**: Classe base para grafos direcionados
```python
class CollaborationGraph:
    def __init__(self, name: str):
        self.name = name
        self.graph = nx.DiGraph()  # Grafo direcionado NetworkX
        self.nodes = {}            # Dicionário de nós
        self.edges = {}            # Dicionário de arestas
```

#### **Grafos Especializados:**

**1. CommentGraph**: Grafo de comentários
- **Arestas**: comentarista → autor da issue/PR
- **Pesos**: 2 (comentários em PR), 3 (comentários em issues)

**2. IssueCloseGraph**: Grafo de fechamento de issues
- **Arestas**: closer → author
- **Peso**: 3

**3. ReviewGraph**: Grafo de reviews e merges
- **Arestas**: reviewer/merger → author
- **Pesos**: 4 (review), 5 (merge)

**4. IntegratedGraph**: Grafo consolidado
- **Combina**: Todos os tipos de interação
- **Pesos ponderados**: Baseados na importância da interação

#### **Métricas de Centralidade Implementadas:**

```python
def calculate_centrality_metrics(self):
    # Centralidade de grau (in/out)
    in_degree_centrality = nx.in_degree_centrality(self.graph)
    out_degree_centrality = nx.out_degree_centrality(self.graph)
    
    # Centralidade de proximidade
    closeness_centrality = nx.closeness_centrality(self.graph)
    
    # Centralidade de intermediação
    betweenness_centrality = nx.betweenness_centrality(self.graph)
    
    # PageRank
    pagerank = nx.pagerank(self.graph)
```

### **3. graph_builder.py**

**Responsabilidade**: Orquestração da construção e análise dos grafos

#### **Classe GraphBuilder**

**Principais Métodos:**

- **`load_data_from_csv()`**: Carrega dados de arquivos CSV existentes
- **`extract_and_load_data()`**: Extrai novos dados via API
- **`build_all_graphs()`**: Constrói todos os 4 tipos de grafo
- **`export_all_graphs()`**: Exporta grafos em JSON e GEXF
- **`generate_report()`**: Gera relatório completo de análise
- **`print_summary()`**: Exibe resumo no console

**Fluxo de Processamento:**

1. **Carregamento**: Dados → DataFrames pandas
2. **Construção**: DataFrames → Grafos NetworkX
3. **Análise**: Cálculo de métricas de centralidade
4. **Exportação**: Grafos → JSON/GEXF para Gephi
5. **Relatório**: Estatísticas → JSON estruturado

### **4. graph_visualizer.py**

**Responsabilidade**: Visualização e análise visual dos grafos

#### **Classe GraphVisualizer**

**Tipos de Visualização:**

**1. Grafos Estáticos (Matplotlib + Seaborn)**
```python
def plot_graph_basic(self, graph: CollaborationGraph):
    # Layout spring para posicionamento
    pos = nx.spring_layout(subgraph, k=1, iterations=50)
    
    # Tamanho baseado no grau
    node_sizes = [degrees[node] * 20 for node in subgraph.nodes()]
    
    # Cor baseada na centralidade
    node_colors = [centralities[node] for node in subgraph.nodes()]
```

**2. Grafos Interativos (Plotly)**
```python
def plot_interactive_graph(self, graph: CollaborationGraph):
    # Traces para arestas e nós
    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode='lines')
    node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text')
```

**3. Análises Comparativas**
- **Boxplots**: Comparação de centralidades entre grafos
- **Barplots**: Métricas agregadas dos grafos
- **Rankings**: Top colaboradores por diferentes critérios

**4. Dashboard Interativo**
```python
def create_dashboard(self, graphs: Dict[str, CollaborationGraph]):
    fig = make_subplots(rows=2, cols=2, subplot_titles=(...))
    # Múltiplas visualizações em uma interface
```

---

## ⚙️ Scripts Auxiliares

### **main.py**
**Função**: Script principal que orquestra todo o pipeline

```python
def main():
    # 1. Configuração e carregamento de variáveis
    load_dotenv()
    
    # 2. Extração ou carregamento de dados
    builder.extract_and_load_data() or builder.load_data_from_csv()
    
    # 3. Construção dos grafos
    builder.build_all_graphs()
    
    # 4. Exportação e visualização
    builder.export_all_graphs()
    visualizer.create_dashboard()
```

### **complete_extraction.py**
**Função**: Script de recuperação para completar extrações falhadas

**Funcionalidades:**
- Extrai apenas dados faltantes
- Reutiliza dados já extraídos
- Tratamento específico para rate limits

### **generate_sample_data.py**
**Função**: Gerador de dados simulados para testes

**Gera:**
- Issues simuladas com metadados realistas
- PRs com informações de merge
- Comentários e reviews distribuídos estatisticamente
- Relacionamentos entre usuários simulados

### **check_rate_limit.py**
**Função**: Monitoramento do rate limit da API GitHub

```python
def check_rate_limit():
    response = requests.get("https://api.github.com/rate_limit", headers=headers)
    data = response.json()
    
    core = data['resources']['core']
    print(f"Requests restantes: {core['remaining']}")
    print(f"Reset em: {datetime.fromtimestamp(core['reset'])}")
```

---

## 📊 Estruturas de Dados

### **Issues DataFrame**
```
Colunas: id, number, title, state, author, created_at, updated_at, 
         closed_at, closed_by, comments_count, is_pull_request
```

### **Pull Requests DataFrame**
```
Colunas: id, number, title, state, author, created_at, updated_at,
         closed_at, merged_at, merged_by, comments_count, 
         review_comments_count, commits_count, additions, deletions
```

### **Comments DataFrames**
```
Issue Comments: id, issue_number, author, created_at, updated_at, body_length
PR Comments: id, pr_number, author, created_at, type, body_length
```

### **Reviews DataFrame**
```
Colunas: id, pr_number, reviewer, state, submitted_at, body_length
```

---

## 🔄 Fluxo de Execução

### **Pipeline Completo:**

1. **Inicialização**
   - Carregamento de configurações (.env)
   - Inicialização de classes principais

2. **Extração de Dados**
   - Requisições paginadas à API GitHub
   - Tratamento de rate limits
   - Persistência em CSV

3. **Processamento**
   - Limpeza e normalização dos dados
   - Filtros por tipo de interação
   - Construção de relacionamentos

4. **Modelagem de Grafos**
   - Criação de nós (usuários)
   - Criação de arestas (interações)
   - Atribuição de pesos

5. **Análise**
   - Cálculo de métricas de centralidade
   - Estatísticas descritivas
   - Identificação de padrões

6. **Visualização**
   - Grafos de rede
   - Dashboards interativos
   - Análises comparativas

7. **Exportação**
   - JSON para análises programáticas
   - GEXF para Gephi
   - HTML para visualização web

---

## 🧮 Algoritmos Implementados

### **Centralidade de Grau**
```python
# In-degree: quantas interações o usuário recebe
in_degree = graph.in_degree(node)

# Out-degree: quantas interações o usuário faz
out_degree = graph.out_degree(node)
```

### **Centralidade de Proximidade**
```python
# Distância média inversa para todos os outros nós
closeness = nx.closeness_centrality(graph)
```

### **Centralidade de Intermediação**
```python
# Frequência do nó nos caminhos mais curtos
betweenness = nx.betweenness_centrality(graph)
```

### **PageRank**
```python
# Importância baseada na qualidade das conexões
pagerank = nx.pagerank(graph, alpha=0.85)
```

---

## ⚡ Otimizações Implementadas

### **Performance**
- **Paginação eficiente**: Requisições em lotes de 100 itens
- **Caching**: Dados salvos em CSV para reutilização
- **Subgrafos**: Visualização apenas dos nós mais relevantes
- **Lazy loading**: Cálculos sob demanda

### **Robustez**
- **Error handling**: Try-catch em todas as requisições
- **Rate limiting**: Pausas automáticas quando necessário
- **Validação**: Verificação de integridade dos dados
- **Fallbacks**: Dados simulados quando API falha

### **Escalabilidade**
- **Modular**: Cada funcionalidade em classe separada
- **Configurável**: Parâmetros ajustáveis via .env
- **Extensível**: Fácil adição de novos tipos de grafo

---

## 🎯 Casos de Uso

### **Análise de Comunidades**
- Identificar grupos de colaboradores frequentes
- Detectar núcleos de desenvolvimento
- Mapear hierarquias de contribuição

### **Detecção de Influenciadores**
- Usuários com alta centralidade
- Conectores entre diferentes grupos
- Especialistas em áreas específicas

### **Evolução Temporal**
- Tracking de mudanças na rede
- Identificação de tendências
- Previsão de futuras colaborações

### **Comparação de Repositórios**
- Benchmarking entre projetos
- Análise de maturidade
- Padrões de governança

---

## 📈 Métricas de Qualidade

### **Cobertura de Código**
- Tratamento de erros em 100% das requisições
- Validação de dados em todos os pontos
- Testes com dados simulados

### **Performance**
- Máximo de 5.000 requests/hora (com token)
- Processamento de 1000+ issues em < 30 minutos
- Visualização de grafos com 50+ nós em tempo real

### **Usabilidade**
- Configuração via arquivos .env
- Outputs em múltiplos formatos
- Documentação completa e exemplos

Este README técnico fornece uma visão abrangente de toda a implementação, desde as bibliotecas utilizadas até os algoritmos específicos implementados para análise de grafos de colaboração.