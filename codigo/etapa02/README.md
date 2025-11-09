# Etapa 2 - Desenvolvimento da Ferramenta
## Trabalho de Teoria dos Grafos

**Implementação da estrutura de grafos conforme especificações da Etapa 2.**

---

## 📋 **Especificações Implementadas**

### **Estrutura de Classes**
- ✅ **AbstractGraph**: Classe abstrata com API comum e atributos compartilhados
- ✅ **AdjacencyMatrixGraph**: Implementação usando matriz de adjacência
- ✅ **AdjacencyListGraph**: Implementação usando listas de adjacência

### **Construtores Obrigatórios**
- ✅ `AdjacencyMatrixGraph(int numVertices)`
- ✅ `AdjacencyListGraph(int numVertices)`

### **API Obrigatória Completa**
- ✅ `int getVertexCount()`
- ✅ `int getEdgeCount()`
- ✅ `boolean hasEdge(int u, int v)`
- ✅ `void addEdge(int u, int v)` (idempotente)
- ✅ `void removeEdge(int u, int v)`
- ✅ `boolean isSucessor(int u, int v)`
- ✅ `boolean isPredessor(int u, int v)`
- ✅ `boolean isDivergent(int u1, int v1, int u2, int v2)`
- ✅ `boolean isConvergent(int u1, int v1, int u2, int v2)`
- ✅ `boolean isIncident(int u, int v, int x)`
- ✅ `int getVertexInDegree(int u)`
- ✅ `int getVertexOutDegree(int u)`
- ✅ `void setVertexWeight(int v, double w)`
- ✅ `double getVertexWeight(int v)`
- ✅ `void setEdgeWeight(int u, int v, double w)`
- ✅ `double getEdgeWeight(int u, int v)`
- ✅ `boolean isConnected()`
- ✅ `boolean isEmptyGraph()`
- ✅ `boolean isCompleteGraph()`

### **Método Adicional**
- ✅ `void exportToGEPHI(String path)` - **Sem dependências externas**

---

## 🚫 **Restrições Atendidas**

- ✅ **Grafos simples**: Não permitem laços nem múltiplas arestas
- ✅ **Idempotência**: `addEdge(u,v)` não duplica arestas
- ✅ **Exceções**: Lançadas para índices inválidos e operações inconsistentes
- ✅ **Sem APIs externas**: Implementação puramente manual

---

## 🗂️ **Estrutura de Arquivos**

```
etapa02/
├── src/
│   ├── AbstractGraph.py          # Classe abstrata base
│   ├── AdjacencyMatrixGraph.py   # Implementação com matriz
│   ├── AdjacencyListGraph.py     # Implementação com listas
│   └── __init__.py              # Módulo Python
├── demo.py                      # Demonstração das funcionalidades
├── test_graphs.py              # Testes unitários rigorosos
└── README.md                   # Esta documentação
```

---

## 🚀 **Como Executar**

### **Demonstração**
```bash
python demo.py
```

### **Testes Unitários**
```bash
python test_graphs.py
```

---

## 🔧 **Uso das Classes**

### **Exemplo Básico**
```python
from src.AdjacencyMatrixGraph import AdjacencyMatrixGraph
from src.AdjacencyListGraph import AdjacencyListGraph

# Cria grafo com 4 vértices
graph_matrix = AdjacencyMatrixGraph(4)
graph_list = AdjacencyListGraph(4)

# Adiciona arestas
graph_matrix.addEdge(0, 1)
graph_matrix.addEdge(1, 2)

# Verifica propriedades
print(f"Vértices: {graph_matrix.getVertexCount()}")
print(f"Arestas: {graph_matrix.getEdgeCount()}")
print(f"Tem aresta (0,1): {graph_matrix.hasEdge(0, 1)}")

# Exporta para Gephi
graph_matrix.exportToGEPHI("meu_grafo.gexf")
```

### **Exemplo com Pesos**
```python
# Define pesos de vértices e arestas
graph_matrix.setVertexWeight(0, 10.5)
graph_matrix.setEdgeWeight(0, 1, 5.0)

# Recupera pesos
peso_vertice = graph_matrix.getVertexWeight(0)
peso_aresta = graph_matrix.getEdgeWeight(0, 1)
```

---

## ✅ **Validações Implementadas**

### **Tratamento de Erros**
```python
# Índices inválidos
graph.addEdge(-1, 0)     # IndexError
graph.addEdge(0, 10)     # IndexError

# Laços não permitidos  
graph.addEdge(1, 1)      # ValueError

# Operações em arestas inexistentes
graph.getEdgeWeight(0, 2)  # ValueError (se aresta não existe)
```

### **Operações Especiais**
```python
# Verifica relações entre arestas
graph.isDivergent(0, 1, 0, 2)    # Mesma origem
graph.isConvergent(1, 3, 2, 3)   # Mesmo destino
graph.isIncident(0, 1, 0)        # Aresta incidente ao vértice

# Propriedades do grafo
graph.isConnected()      # Conectividade
graph.isEmptyGraph()     # Sem arestas
graph.isCompleteGraph()  # Todas as arestas possíveis
```

---

## 🎯 **Características Técnicas**

### **Herança e Abstração**
- Uso correto de classe abstrata `AbstractGraph`
- Métodos abstratos implementados nas subclasses
- Compartilhamento de código comum na classe base

### **Complexidade Computacional**

| Operação | Matriz | Lista |
|----------|--------|-------|
| `addEdge` | O(1) | O(1) |
| `hasEdge` | O(1) | O(1) |
| `getVertexOutDegree` | O(V) | O(1) |
| `getVertexInDegree` | O(V) | O(V) |
| `isConnected` | O(V²) | O(V+E) |

### **Eficiência de Memória**
- **Matriz**: O(V²) - Ideal para grafos densos
- **Lista**: O(V+E) - Ideal para grafos esparsos

---

## 📝 **Conformidade com Especificações**

| **Requisito** | **Status** | **Implementação** |
|---------------|------------|-------------------|
| ✅ Classe AbstractGraph | **Completo** | API comum + validações |
| ✅ AdjacencyMatrixGraph | **Completo** | Matriz booleana |
| ✅ AdjacencyListGraph | **Completo** | Dict de Sets |
| ✅ Construtores obrigatórios | **Completo** | Validação de parâmetros |
| ✅ API completa (19 métodos) | **Completo** | Todas as funcionalidades |
| ✅ Restrições (grafos simples) | **Completo** | Sem laços/múltiplas |
| ✅ Tratamento de exceções | **Completo** | IndexError/ValueError |
| ✅ Exportação Gephi | **Completo** | **Sem APIs externas** |
| ✅ Herança e abstração | **Completo** | Código limpo e claro |

---

## 🎉 **Resultado Final**

**Protótipo funcional** implementado conforme todas as especificações da Etapa 2:

- ✅ **Código versionado** no GitHub
- ✅ **API completa** implementada
- ✅ **Duas representações** de grafos funcionais
- ✅ **Testes rigorosos** validando corretude
- ✅ **Documentação** clara e exemplos práticos
- ✅ **Sem dependências externas**

**Pronto para uso e avaliação acadêmica!** 🎓✨