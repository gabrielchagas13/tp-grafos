# Ferramenta de Grafos — Etapa 02

Projeto em Python: implementação de uma estrutura de grafos simples com a API pedida.

Principais arquivos
- `src/graph.py` — implementação da classe `Graph` e métodos exigidos.
- `tests/test_graph.py` — testes automatizados com pytest.
- `requirements.txt` — dependências (networkx para export para GEXF e pytest para testes).

- `src/graph.py` — implementação da classe `Graph` e métodos exigidos.
- `tests/test_graph.py` — testes automatizados com pytest.
- `requirements.txt` — dependências (pytest para testes). A exportação GEXF foi implementada sem bibliotecas externas.

Como usar
1. Criar um ambiente virtual Python (recomendado).
2. Instalar dependências:

```powershell
pip install -r requirements.txt
```

3. Exemplo rápido:

```python
from src.graph import Graph
g = Graph(4, directed=True)
g.addEdge(0,1)
g.addEdge(1,2)
print(g.getVertexCount(), g.getEdgeCount())
g.exportToGEPHI('out.gexf')
```

Testes
```powershell
pytest -q
```

Notas
- `isConnected` usa conectividade fraca (trata o grafo como não direcionado).
- `isCompleteGraph` verifica que todo par ordenado distinto (u,v) tem aresta u->v.
