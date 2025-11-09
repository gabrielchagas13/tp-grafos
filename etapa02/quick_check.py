from src.adjacency_list_graph import AdjacencyListGraph
from src.adjacency_matrix_graph import AdjacencyMatrixGraph

for GraphClass in (AdjacencyListGraph, AdjacencyMatrixGraph):
    g = GraphClass(4, directed=True)
    g.addEdge(0,1)
    g.addEdge(0,2)
    g.setEdgeWeight(0,1,2.5)
    g.setVertexWeight(3, 1.5)
    print(GraphClass.__name__, "vertices:", g.getVertexCount(), "edges:", g.getEdgeCount())
    print("hasEdge(0,1):", g.hasEdge(0,1), "edgeWeight:", g.getEdgeWeight(0,1))
    print("vertexWeight(3):", g.getVertexWeight(3))
    # exportar um GEXF para abrir no Gephi
    g.exportToGEPHI('out_{}.gexf'.format(GraphClass.__name__))
print('arquivos out_AdjacencyListGraph.gexf e out_AdjacencyMatrixGraph.gexf gerados (se não houver erro).')
