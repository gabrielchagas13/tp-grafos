# Análise de Grafos de Colaboração - MMDetection
## Trabalho de Teoria dos Grafos - Etapa 1

Este projeto implementa a análise de grafos de colaboração do repositório **open-mmlab/mmdetection** conforme as especificações da Etapa 1 do trabalho de Teoria dos Grafos.

## 📋 Objetivo

Analisar as interações entre usuários no repositório MMDetection através da construção de grafos direcionados que representam diferentes tipos de colaboração:

1. **Grafo de Comentários**: Interações através de comentários em issues e pull requests
2. **Grafo de Fechamento de Issues**: Relações entre quem abre e quem fecha issues
3. **Grafo de Reviews/Merges**: Interações através de reviews, aprovações e merges de PRs
4. **Grafo Integrado**: Combinação ponderada de todas as interações

## 🏗️ Estrutura do Projeto

```
etapa01/
├── src/
│   ├── github_extractor.py    # Extração de dados da API do GitHub
│   ├── graph_models.py        # Classes para modelagem dos grafos
│   ├── graph_builder.py       # Construção e análise dos grafos
│   └── graph_visualizer.py    # Visualização dos grafos
├── data/                      # Dados extraídos (CSV)
├── output/                    # Resultados da análise
├── main.py                    # Script principal
├── requirements.txt           # Dependências Python
├── .env.example              # Exemplo de configuração
└── README.md                 # Este arquivo
```

## 🚀 Instalação e Configuração

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Token do GitHub (Opcional)

Para extrair dados diretamente do GitHub, crie um arquivo `.env`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione seu token do GitHub:

```
GITHUB_TOKEN=seu_token_aqui
REPO_OWNER=open-mmlab
REPO_NAME=mmdetection
MAX_ISSUES=1000
MAX_PRS=1000
MAX_COMMENTS=5000
```

**Como obter um token do GitHub:**
1. Acesse GitHub → Settings → Developer settings → Personal access tokens
2. Gere um novo token com permissões de leitura de repositórios públicos
3. Copie o token para o arquivo `.env`

### 3. Executar Análise

```bash
python main.py
```

## 📊 Modelagem dos Grafos

### Regras de Construção

- **Nós**: Cada usuário é representado como um nó
- **Arestas**: Interações direcionadas entre usuários
- **Pesos**: Diferentes tipos de interação têm pesos distintos

### Pesos das Interações

| Tipo de Interação | Peso | Descrição |
|-------------------|------|-----------|
| Comentário em PR | 2 | Comentário em pull request |
| Comentário em Issue | 3 | Comentário em issue aberta por outro usuário |
| Review de PR | 4 | Review, aprovação ou solicitação de mudanças |
| Merge de PR | 5 | Merge de pull request |
| Fechamento de Issue | 3 | Fechamento de issue aberta por outro usuário |

### Grafos Construídos

1. **Grafo de Comentários**
   - Arestas: usuário que comenta → autor da issue/PR
   - Peso: 2 (comentários em PR) ou 3 (comentários em issues)

2. **Grafo de Fechamento de Issues**
   - Arestas: usuário que fecha → autor da issue
   - Peso: 3

3. **Grafo de Reviews/Merges**
   - Arestas: reviewer/merger → autor do PR
   - Peso: 4 (review) ou 5 (merge)

4. **Grafo Integrado**
   - Combina todas as interações com pesos apropriados
   - Permite análise holística da rede de colaboração

## 📈 Métricas Calculadas

### Métricas de Centralidade

- **Centralidade de Grau** (in/out): Número de conexões entrantes/saintes
- **Centralidade de Proximidade**: Proximidade média a todos os outros nós
- **Centralidade de Intermediação**: Frequência em caminhos mais curtos
- **PageRank**: Importância baseada na qualidade das conexões

### Métricas do Grafo

- **Densidade**: Proporção de arestas existentes vs. possíveis
- **Conectividade**: Se o grafo é fracamente conectado
- **Distribuições**: Análise estatística das centralidades

## 📁 Arquivos Gerados

### Dados Extraídos (`data/`)
- `issues_mmdetection.csv`: Dados das issues
- `pull_requests_mmdetection.csv`: Dados dos pull requests
- `issue_comments_mmdetection.csv`: Comentários das issues
- `pr_reviews_mmdetection.csv`: Reviews dos PRs
- `pr_comments_mmdetection.csv`: Comentários dos PRs

### Resultados da Análise (`output/`)
- `analysis_report.json`: Relatório completo da análise
- `*_graph.json`: Grafos em formato JSON
- `*_graph.gexf`: Grafos em formato GEXF (Gephi)
- `*.png`: Visualizações estáticas
- `*.html`: Visualizações interativas
- `dashboard.html`: Dashboard completo

## 🎨 Visualizações

### 1. Visualizações Estáticas (PNG)
- Grafos básicos de cada tipo de interação
- Comparação de métricas entre grafos
- Ranking de top colaboradores
- Distribuições de centralidade

### 2. Visualizações Interativas (HTML)
- Grafos interativos com informações detalhadas
- Dashboard com múltiplas visualizações
- Navegação e zoom nos grafos

### 3. Arquivos para Gephi (GEXF)
- Importação direta no Gephi para análises avançadas
- Preserva todas as métricas calculadas
- Permite layouts e análises personalizadas

## 🔍 Interpretação dos Resultados

### Usuários Centrais
Usuários com alta centralidade são importantes na rede de colaboração:
- **Alto grau de entrada**: Recebem muitas interações (autores ativos)
- **Alto grau de saída**: Fazem muitas interações (reviewers/colaboradores)
- **Alta intermediação**: Conectam diferentes partes da rede

### Padrões de Colaboração
O grafo integrado revela:
- Núcleos de colaboração intensa
- Usuários ponte entre diferentes grupos
- Assimetrias nas relações de colaboração

### Qualidade das Interações
Pesos diferentes permitem identificar:
- Colaboradores superficiais (apenas comentários)
- Colaboradores técnicos (reviews e merges)
- Mantenedores ativos (fechamento de issues)

## 🛠️ Troubleshooting

### Erro de Rate Limit
- O script aguarda automaticamente quando atinge o rate limit
- Use um token do GitHub para aumentar o limite
- Reduza MAX_ISSUES e MAX_PRS no .env

### Erro de Memória
- Reduza o número máximo de issues/PRs
- Processe dados em lotes menores
- Use filtros para focar em períodos específicos

### Grafos Vazios
- Verifique se os dados foram extraídos corretamente
- Confirme se o repositório tem atividade suficiente
- Ajuste os filtros de data se necessário

## 📚 Dependências Principais

- **NetworkX**: Análise e manipulação de grafos
- **Pandas**: Manipulação de dados
- **Matplotlib/Seaborn**: Visualizações estáticas
- **Plotly**: Visualizações interativas
- **Requests**: API do GitHub
- **python-dotenv**: Configurações


---

**Repositório analisado**: [open-mmlab/mmdetection](https://github.com/open-mmlab/mmdetection) (37k+ ⭐)

**Desenvolvido por**: Gabriel Chagas Lage, Marcus Vinicius, Arthur Pedra  
**Curso**: Engenharia de Software
**Matéria**: Teoria dos Grafos  