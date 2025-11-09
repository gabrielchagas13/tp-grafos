# ETAPA 3 - ANÁLISE DO REPOSITÓRIO BASEADA EM DADOS

## 📋 Visão Geral

A **Etapa 3** é a fase final do projeto de análise de grafos, focada na **análise avançada da rede de colaboração** e **geração de visualizações**. Esta etapa utiliza os dados extraídos na Etapa 1 e as estruturas de grafos implementadas na Etapa 2 para realizar uma análise completa e profissional da colaboração no repositório mmdetection.

## 🎯 Objetivos

1. **Carregar e integrar** os dados CSV da Etapa 1
2. **Construir grafo** de colaboração com pesos baseados nas interações
3. **Calcular métricas avançadas** de centralidade e análise de redes
4. **Gerar visualizações profissionais** dos resultados
5. **Produzir relatórios** detalhados e insights automáticos

## 🏗️ Arquitetura

### Estrutura de Diretórios
```
etapa03/
├── main.py                     # Script principal de execução
├── requirements.txt            # Dependências Python
├── README.md                   # Esta documentação
├── src/                        # Código fonte
│   ├── __init__.py
│   ├── AbstractGraph.py        # Classe base abstrata (da Etapa 2)
│   ├── AdjacencyListGraph.py   # Implementação com listas (da Etapa 2)
│   ├── DataLoader.py           # Carregamento dos dados da Etapa 1
│   ├── GraphAnalyzer.py        # Análises avançadas de grafos
│   └── GraphVisualizer.py      # Geração de gráficos e visualizações
└── output/                     # Resultados gerados (criado automaticamente)
    ├── centralidade_comparacao.png
    ├── metricas_rede.png
    ├── distribuicao_graus.png
    ├── analise_comunidades.png
    ├── resultados_completos.json
    └── relatorio_resumo.json
```

## 🔧 Componentes Principais

### 1. DataLoader (src/DataLoader.py)

**Responsabilidade**: Carrega dados CSV da Etapa 1 e constrói grafo integrado.

**Funcionalidades**:
- Carrega CSVs de issues, PRs, comentários e reviews
- Mapeia usuários para IDs numéricos
- Constrói grafo com sistema de pesos:
  - Comentários: peso 2
  - Issues/PRs comentadas: peso 3
  - Reviews: peso 4
  - Merges: peso 5

**Métodos principais**:
- `load_csv_data()`: Carrega todos os CSVs
- `build_collaboration_graph()`: Constrói grafo integrado
- `get_user_mapping()`: Retorna mapeamento ID ↔ username

### 2. GraphAnalyzer (src/GraphAnalyzer.py)

**Responsabilidade**: Implementa algoritmos avançados de análise de grafos.

**Métricas de Centralidade**:
- **Centralidade de Grau**: Número de conexões diretas
- **Centralidade de Intermediação**: Importância como ponte entre outros nós
- **Centralidade de Proximidade**: Proximidade média a todos os outros nós
- **PageRank**: Algoritmo de ranking baseado em importância relativa
- **Centralidade de Autovetor**: Centralidade baseada na qualidade das conexões

**Métricas da Rede**:
- **Densidade**: Proporção de arestas existentes vs possíveis
- **Grau Médio**: Média de conexões por usuário
- **Coeficiente de Clustering**: Tendência de formação de grupos
- **Assortatividade**: Tendência de usuários similares se conectarem

**Análise de Comunidades**:
- **Modularidade**: Qualidade da divisão em comunidades
- **Proporção de Ligações entre Grupos**: Conectividade inter-comunitária

### 3. GraphVisualizer (src/GraphVisualizer.py)

**Responsabilidade**: Gera visualizações profissionais e relatórios.

**Visualizações Geradas**:

1. **Comparação de Centralidades** (`centralidade_comparacao.png`)
   - Gráfico de barras comparando top 15 usuários
   - 5 métricas de centralidade normalizadas
   - Cores profissionais e legendas claras

2. **Métricas da Rede** (`metricas_rede.png`)
   - Dashboard com 4 painéis
   - Densidade, clustering, assortatividade
   - Métricas estruturais (vértices, arestas, grau médio)

3. **Distribuição de Graus** (`distribuicao_graus.png`)
   - Histograma da distribuição
   - Ranking dos top 15 usuários por grau
   - Separação entre grau de entrada e saída

4. **Análise Comunitária** (`analise_comunidades.png`)
   - Modularidade e interpretação automática
   - Proporção de ligações entre grupos
   - Insights sobre estrutura comunitária

**Relatórios**:
- **JSON Completo**: Todos os dados numéricos
- **Resumo Executivo**: Top usuários e insights automáticos

## 🚀 Como Executar

### Pré-requisitos

1. **Python 3.8+** instalado
2. **Etapa 1** executada com dados CSV gerados
3. **Dependências** instaladas

### Instalação das Dependências

```bash
cd etapa03
pip install -r requirements.txt
```

### Execução

```bash
python main.py
```

### Saída Esperada

O script irá:

1. ✅ Carregar dados CSV da Etapa 1
2. 🔄 Construir grafo de colaboração (pode levar alguns minutos)
3. 📊 Calcular métricas de centralidade e rede
4. 🎨 Gerar 4 gráficos PNG profissionais
5. 📋 Criar relatórios JSON detalhados
6. 💡 Exibir resumo executivo com insights

## 📊 Interpretação dos Resultados

### Métricas de Centralidade

- **Alto grau**: Usuário com muitas conexões diretas
- **Alta intermediação**: Usuário que conecta diferentes grupos
- **Alta proximidade**: Usuário "central" na rede
- **Alto PageRank**: Usuário influente conectado a outros influentes
- **Alto autovetor**: Usuário conectado a usuários importantes

### Métricas da Rede

- **Densidade alta** (>0.05): Rede muito conectada
- **Clustering alto** (>0.3): Grupos coesos identificados  
- **Assortatividade positiva**: Usuários similares colaboram mais
- **Assortatividade negativa**: Usuários diferentes colaboram mais

### Modularidade

- **> 0.3**: Estrutura comunitária forte
- **0.1 - 0.3**: Estrutura moderada
- **< 0.1**: Estrutura comunitária fraca

## 🔬 Metodologia

### Sistema de Pesos

O grafo é construído com pesos que refletem diferentes tipos de colaboração:

```
Comentário → +2 pontos
Issue/PR comentada → +3 pontos  
Review de PR → +4 pontos
Merge de PR → +5 pontos
Fechamento de Issue → +3 pontos
```

Este sistema valoriza mais as ações que requerem maior envolvimento e responsabilidade.

### Algoritmos Implementados

- **PageRank**: Implementação personalizada com amortecimento 0.85
- **Centralidade de Autovetor**: Método da potência com normalização
- **Intermediação**: Algoritmo de Brandes otimizado
- **Modularidade**: Baseada na qualidade da estrutura comunitária

## 📈 Casos de Uso

### Para Gestores de Projeto

- **Identificar colaboradores chave** através das centralidades
- **Entender estrutura de equipes** via análise comunitária
- **Avaliar distribuição de trabalho** através dos graus

### Para Pesquisadores

- **Análise de redes sociais** em projetos open source
- **Padrões de colaboração** em desenvolvimento de software
- **Métricas de engajamento** da comunidade

### Para Desenvolvedores

- **Identificar especialistas** em áreas específicas
- **Entender fluxos de comunicação** no projeto
- **Avaliar importância** de diferentes contribuidores

## 🛠️ Personalização

### Modificar Pesos

Edite `DataLoader.py`, método `build_collaboration_graph()`:

```python
add_edge_weight(comment_author, issue_author, 2)  # Peso do comentário
add_edge_weight(issue_author, comment_author, 3)  # Peso da issue comentada
```

### Adicionar Métricas

Estenda `GraphAnalyzer.py`:

```python
def nova_metrica(self, graph: AbstractGraph) -> Dict[str, float]:
    # Implementação da nova métrica
    pass
```

### Customizar Visualizações

Modifique `GraphVisualizer.py` para ajustar:
- Cores e estilos
- Número de elementos mostrados  
- Layout dos gráficos
- Métricas incluídas

## ⚡ Performance

### Complexidade Computacional

- **Carregamento**: O(n) onde n = registros CSV
- **Construção do grafo**: O(n) 
- **Centralidade de grau**: O(V)
- **Centralidade de intermediação**: O(V³)
- **PageRank**: O(V² × iterações)
- **Visualização**: O(V log V) para ordenações

### Otimizações

- Uso de estruturas eficientes (listas de adjacência)
- Algoritmos otimizados para grafos esparsos
- Normalização de valores para melhor visualização
- Cache de resultados intermediários

## 🤝 Integração com Outras Etapas

### Dependências da Etapa 1

- CSVs de dados: `issues_mmdetection.csv`, `pull_requests_mmdetection.csv`, etc.
- Localização esperada: `../etapa01/data/`

### Dependências da Etapa 2  

- Classes base: `AbstractGraph.py`, `AdjacencyListGraph.py`
- Copiadas para `src/` na Etapa 3
- API completa de 19 métodos utilizada

### Saídas Produzidas

- **Gráficos PNG**: Para relatórios e apresentações
- **Dados JSON**: Para análises posteriores ou integração
- **Insights automáticos**: Para documentação do projeto

## 🔍 Troubleshooting

### Erros Comuns

1. **"Nenhum dado encontrado"**
   - Verifique se a Etapa 1 foi executada
   - Confirme se os CSVs estão em `../etapa01/data/`

2. **"Grafo vazio"**
   - Dados CSV podem estar corrompidos
   - Verifique formato das colunas nos CSVs

3. **"Erro de dependência"**
   - Execute: `pip install -r requirements.txt`
   - Verifique versão do Python (3.8+)

4. **Gráficos não gerados**
   - Verifique se matplotlib está instalado
   - Confirme permissões de escrita no diretório

### Debug

Para debug detalhado, modifique `main.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 Referências Acadêmicas

- **Newman, M.E.J.** (2010). Networks: An Introduction. Oxford University Press.
- **Brandes, U.** (2001). A faster algorithm for betweenness centrality. Journal of Mathematical Sociology.
- **Page, L. et al.** (1999). The PageRank Citation Ranking: Bringing Order to the Web.
- **Bonacich, P.** (1987). Power and centrality: A family of measures. American Journal of Sociology.

---

**Trabalho de Teoria dos Grafos - Etapa 3**  
*Análise avançada de redes de colaboração em repositórios GitHub*