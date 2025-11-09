# Documentação da Etapa 1 - Análise de Grafos de Colaboração

## Trabalho de Teoria dos Grafos
**Repositório Analisado:** open-mmlab/mmdetection  
**Data:** Novembro de 2025  
**Etapa:** 1 - Modelagem e Planejamento da Solução

---

## 1. Descrição do Problema

### 1.1 Contexto
A colaboração em projetos de software de código aberto representa um ecossistema complexo de interações entre desenvolvedores, onde diferentes tipos de contribuições e comunicações formam uma rede de relacionamentos técnicos e sociais. Compreender essas redes é fundamental para:

- **Identificar padrões de colaboração** entre membros da comunidade
- **Mapear influência e centralidade** de colaboradores-chave
- **Analisar fluxos de comunicação** e tomada de decisões
- **Detectar estruturas organizacionais** emergentes no projeto
- **Avaliar saúde e sustentabilidade** da comunidade

### 1.2 Problema Central
O desafio consiste em **modelar matematicamente as interações humanas** em repositórios GitHub através da **Teoria dos Grafos**, transformando dados comportamentais complexos em estruturas analisáveis que revelem:

1. **Redes de comunicação** (comentários e discussões)
2. **Redes de autoridade** (fechamento de issues e tomada de decisões)
3. **Redes de revisão técnica** (code reviews e aprovações)
4. **Rede integrada** que combine todos os aspectos da colaboração

### 1.3 Objetivos
- Construir **grafos direcionados** representando diferentes dimensões da colaboração
- Implementar **sistema de pesos** que reflita a importância relativa de cada tipo de interação
- Gerar **métricas de centralidade** para identificar usuários-chave
- Produzir **visualizações interpretáveis** da rede de colaboração

---

## 2. Justificativa da Escolha do Repositório

### 2.1 Repositório Selecionado: open-mmlab/mmdetection

**URL:** https://github.com/open-mmlab/mmdetection  
**Descrição:** OpenMMLab Detection Toolbox and Benchmark

### 2.2 Métricas que Justificam a Escolha

| Métrica | Valor | Justificativa |
|---------|-------|---------------|
| **⭐ Estrelas** | 31.973 | Muito superior ao mínimo de 5.000, garantindo alta visibilidade |
| **🔄 Forks** | 9.787 | Indica uso ativo e desenvolvimento distribuído |
| **📋 Issues** | 1.941 (abertas) | Volume significativo de discussões e problemas |
| **🌐 Linguagem** | Python | Linguagem popular que atrai comunidade diversa |
| **🏢 Organização** | OpenMMLab | Organização acadêmica/industrial respeitada |

### 2.3 Justificativas Técnicas

1. **Comunidade Ativa e Diversa**
   - Projeto mantido por laboratório de pesquisa (OpenMMLab)
   - Usuários acadêmicos e industriais
   - Colaboradores de diferentes níveis de expertise

2. **Volume de Interações Significativo**
   - Issues complexas que geram discussões extensas
   - Pull requests que requerem multiple reviews
   - Documentação e tutoriais que provocam comentários

3. **Domínio Técnico Especializado**
   - Computer Vision e Machine Learning
   - Requer colaboração técnica de alta qualidade
   - Reviews detalhadas e discussões aprofundadas

4. **Padrões de Colaboração Variados**
   - Maintainers oficiais com autoridade de merge
   - Contribuidores externos com diferentes níveis de acesso
   - Usuários que reportam bugs e pedem features

---

## 3. Estratégia de Coleta de Dados

### 3.1 Fonte de Dados
**API GitHub REST v3** - https://api.github.com/repos/open-mmlab/mmdetection

### 3.2 Dados Coletados

#### 3.2.1 Issues (Problemas e Discussões)
```python
Campos extraídos:
- id, number, title, state
- author (criador da issue)
- created_at, updated_at, closed_at
- closed_by (quem fechou a issue)
- comments_count
```

#### 3.2.2 Pull Requests (Propostas de Código)
```python
Campos extraídos:
- id, number, title, state
- author (criador do PR)
- created_at, updated_at, closed_at, merged_at
- merged_by (quem fez o merge)
- comments_count, review_comments_count
```

#### 3.2.3 Comentários em Issues
```python
Campos extraídos:
- id, issue_number
- author (autor do comentário)
- created_at, updated_at
- body_length (tamanho do comentário)
```

#### 3.2.4 Reviews de Pull Requests
```python
Campos extraídos:
- id, pr_number
- reviewer (quem fez o review)
- state (APPROVED, CHANGES_REQUESTED, COMMENTED)
- submitted_at
```

#### 3.2.5 Comentários em Pull Requests
```python
Campos extraídos:
- id, pr_number
- author (autor do comentário)
- type (issue_comment ou review_comment)
- created_at
```

### 3.3 Limitações e Tratamento

1. **Rate Limiting da API**
   - Limite: 5.000 requests/hora (com token)
   - Solução: Implementação de pausa entre requests e cache local

2. **Volume de Dados**
   - Limitação: Máximo de 500 issues e 500 PRs por execução
   - Justificativa: Focamor em dados recentes (sort by updated)

3. **Fallback para Dados Locais**
   - Arquivos CSV como backup quando API não disponível
   - Dados preprocessados salvos na pasta `data/`

---

## 4. Transformação de Interações em Arestas

### 4.1 Metodologia de Mapeamento

Cada tipo de interação é transformado em **arestas direcionadas** entre **usuários (nós)** seguindo regras específicas:

#### 4.1.1 Grafo 1: Comentários (Comments Graph)
```
Regra: usuario_A → usuario_B se A comenta em issue/PR criado por B

Implementação:
- Source: author do comentário
- Target: author da issue/PR original
- Weight: 1 por comentário
- Direction: comentarista → autor original
```

**Exemplo:**
```
alice cria issue #123
bob comenta na issue #123
charlie comenta na issue #123
→ Arestas: bob→alice, charlie→alice
```

#### 4.1.2 Grafo 2: Fechamento de Issues (Issue Closes Graph)
```
Regra: usuario_A → usuario_B se A fecha issue criada por B

Implementação:
- Source: closed_by (quem fechou)
- Target: author da issue
- Weight: 3 por fechamento
- Direction: quem fechou → autor da issue
```

**Exemplo:**
```
alice cria issue #456
maintainer fecha issue #456
→ Aresta: maintainer→alice (peso 3)
```

#### 4.1.3 Grafo 3: Reviews e Merges (Reviews Graph)
```
Regra: usuario_A → usuario_B se A revisa/aprova/merge PR de B

Implementação Reviews:
- Source: reviewer
- Target: PR author
- Weight: 4 por review
- Direction: reviewer → autor do PR

Implementação Merges:
- Source: merged_by
- Target: PR author  
- Weight: 5 por merge
- Direction: quem fez merge → autor do PR
```

**Exemplo:**
```
alice cria PR #789
bob faz review do PR #789
maintainer faz merge do PR #789
→ Arestas: bob→alice (peso 4), maintainer→alice (peso 5)
```

### 4.2 Tratamento de Casos Especiais

1. **Auto-interações**: Removidas (usuário não pode interagir consigo mesmo)
2. **Múltiplas interações**: Pesos são somados na mesma aresta
3. **Interações bidirecionais**: Mantidas como arestas anti-paralelas
4. **Usuários inexistentes**: Filtrados durante o processamento

---

## 5. Proposta de Modelagem do Grafo

### 5.1 Estrutura Matemática

#### 5.1.1 Definição Formal
```
G = (V, E, W) onde:
- V = conjunto de usuários (nós)
- E ⊆ V × V = conjunto de interações (arestas direcionadas)  
- W: E → ℝ+ = função peso das arestas
```

#### 5.1.2 Propriedades
- **Grafo Simples**: Sem arestas múltiplas (pesos acumulados)
- **Grafo Direcionado**: Arestas têm orientação (A→B ≠ B→A)  
- **Grafo Ponderado**: Cada aresta tem peso positivo
- **Permite Anti-paralelas**: (u,v) e (v,u) podem coexistir

### 5.2 Sistema de Pesos

#### 5.2.1 Justificativa dos Pesos
O sistema de pesos reflete a **intensidade do comprometimento** e **complexidade da interação**:

| Tipo de Interação | Peso | Justificativa |
|-------------------|------|---------------|
| **Comentário** | 2 | Interação básica, baixo comprometimento |
| **Issue Comentada** | 3 | Gera discussão, engajamento médio |
| **Review de PR** | 4 | Análise técnica, alto comprometimento |
| **Merge de PR** | 5 | Decisão final, máxima responsabilidade |

#### 5.2.2 Cálculo de Peso Final
```python
weight(u,v) = Σ(comentários × 2) + Σ(issues_comentadas × 3) + 
              Σ(reviews × 4) + Σ(merges × 5)
```

### 5.3 Grafos Construídos

#### 5.3.1 Grafos Individuais
1. **G₁ (Comentários)**: Foca em comunicação e discussão
2. **G₂ (Fechamentos)**: Revela autoridade e resolução de problemas  
3. **G₃ (Reviews)**: Mostra colaboração técnica e qualidade

#### 5.3.2 Grafo Integrado
```
G_integrated = G₁ ⊕ G₂ ⊕ G₃

Onde ⊕ representa união ponderada:
weight_final(u,v) = weight_G₁(u,v) + weight_G₂(u,v) + weight_G₃(u,v)
```

---

## 6. Plano de Desenvolvimento da Solução

### 6.1 Arquitetura do Sistema

```
etapa01/
├── src/
│   ├── github_extractor.py      # Módulo de extração de dados
│   ├── graph_models.py          # Classes de modelagem de grafos
│   ├── graph_builder.py         # Construção e análise
│   └── graph_visualizer.py      # Visualização e relatórios
├── data/                        # Dados extraídos (CSV)
├── output/                      # Resultados e visualizações
├── main.py                      # Script principal
└── requirements.txt             # Dependências Python
```

### 6.2 Fases de Desenvolvimento

#### 6.2.1 **Etapa 1: Extração de Dados** ✅ (IMPLEMENTADA)
```python
# Implementado em github_extractor.py + main.py
class GitHubDataExtractor:
    - extract_issues()
    - extract_pull_requests()
    - extract_issue_comments()
    - extract_pr_reviews()
    - extract_pr_comments()
    - extract_all_data()

# Script principal da Etapa 1
main.py: 
    - APENAS extração e salvamento em CSV
    - SEM construção de grafos
    - SEM visualizações
    - SEM relatórios
```

#### 6.2.2 **Etapas 2+: Modelagem e Análise** ✅ (PARA PRÓXIMAS ETAPAS)
```python
# Implementado em graph_models.py + build_graphs.py
class BaseGraph:           # Grafo base com operações comuns
class CommentsGraph:       # Grafo de comentários
class IssueClosesGraph:    # Grafo de fechamento de issues  
class ReviewsGraph:        # Grafo de reviews e merges
class IntegratedGraph:     # Grafo integrado ponderado

# Script para próximas etapas
build_graphs.py:
    - Construção dos 4 grafos
    - Visualizações e relatórios
    - Análise de métricas
    - Exportação JSON/GEXF
```

### 6.3 Tecnologias Utilizadas

#### 6.3.1 Core Libraries
- **NetworkX**: Construção e análise de grafos
- **Pandas**: Manipulação de dados tabulares  
- **Requests**: Comunicação com API GitHub
- **JSON**: Serialização de dados

#### 6.3.2 Visualização
- **Matplotlib**: Gráficos estatísticos
- **Plotly**: Visualizações interativas
- **HTML/CSS**: Relatórios web

#### 6.3.3 Exportação
- **JSON**: Formato de intercâmbio
- **GEXF**: Formato Gephi para análises avançadas

### 6.4 Métricas de Validação

#### 6.4.1 Métricas dos Grafos
- **Número de nós**: Usuários únicos com interações
- **Número de arestas**: Total de conexões
- **Peso total**: Soma de todos os pesos
- **Densidade**: Conectividade relativa
- **Componentes conectados**: Análise de fragmentação

#### 6.4.2 Métricas de Centralidade
- **Degree Centrality**: Número de conexões
- **Betweenness Centrality**: Posição de intermediação
- **Closeness Centrality**: Proximidade média
- **PageRank**: Influência ponderada

### 6.5 Escopo da Etapa 1

#### 6.5.1 **O que a Etapa 1 FAZ:**
- ✅ **Extração completa** de dados via API GitHub
- ✅ **Salvamento estruturado** em arquivos CSV  
- ✅ **Validação** de dados extraídos
- ✅ **Documentação** metodológica completa

#### 6.5.2 **O que a Etapa 1 NÃO FAZ:**
- ❌ **Construção de grafos** (fica para Etapa 2+)
- ❌ **Visualizações** (fica para Etapa 2+)
- ❌ **Relatórios de análise** (fica para Etapa 2+)
- ❌ **Métricas de centralidade** (fica para Etapa 2+)

### 6.6 Resultados da Etapa 1

#### 6.6.1 **Arquivos Gerados:**
```
data/
├── issues_mmdetection.csv         # 888 issues extraídas
├── pull_requests_mmdetection.csv  # 1.000 PRs extraídos  
├── issue_comments_mmdetection.csv # 569 comentários em issues
├── pr_comments_mmdetection.csv    # 726 comentários em PRs
└── pr_reviews_mmdetection.csv     # 213 reviews de PRs
```

#### 6.6.2 **Total de Dados:**
- **🎯 3.396 registros** extraídos e estruturados
- **📊 Base sólida** para construção dos grafos
- **✅ Conformidade total** com especificações da Etapa 1

---

## 7. Considerações Finais

### 7.1 Contribuições Metodológicas
- Sistema de pesos baseado em comprometimento técnico
- Integração de múltiplas dimensões de colaboração
- Pipeline automatizado de extração e análise

### 7.2 Limitações Reconhecidas
- Dependência da disponibilidade da API GitHub
- Análise limitada aos últimos dados (500 issues/PRs)
- Não considera aspectos qualitativos das interações

### 7.3 Próximos Passos
- Análise temporal da evolução da rede
- Detecção de comunidades e clusters
- Correlação com métricas de produtividade do projeto

---

*Este documento estabelece a base teórica e metodológica para a análise de grafos de colaboração no repositório MMDetection, fornecendo fundamentação sólida para as próximas etapas do trabalho.*