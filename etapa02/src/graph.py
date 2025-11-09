"""
Implementação de uma estrutura de grafos simples (direcionado por padrão).

API requerida (métodos implementados):
- getVertexCount
- getEdgeCount
- hasEdge
- addEdge
- removeEdge
- isSucessor
- isPredessor
- isDivergent
- isConvergent
- isIncident
- getVertexInDegree
- getVertexOutDegree
- setVertexWeight
- getVertexWeight
- setEdgeWeight
- getEdgeWeight
- isConnected
- isEmptyGraph
- isCompleteGraph
- exportToGEPHI

Restrições:
- Grafos simples: sem laços nem arestas múltiplas
- addEdge é idempotente
- Lançam-se exceções para índices inválidos e operações inconsistentes

Observações:
- isConnected utiliza conectividade fraca (trata o grafo como não direcionado)
"""
from typing import List, Set, Dict, Tuple


class Graph:
    def __init__(self, n_vertices: int = 0, directed: bool = True):
        if n_vertices < 0:
            raise ValueError("n_vertices must be non-negative")
        self._n = n_vertices
        self.directed = directed
        # adjacency: list of sets of neighbors (outgoing)
        self._adj: List[Set[int]] = [set() for _ in range(self._n)]
        # edge weights as dict (u,v) -> float
        self._edge_weights: Dict[Tuple[int, int], float] = {}
        # vertex weights list
        self._vertex_weights: List[float] = [0.0 for _ in range(self._n)]

    # --- helpers ---
    def _validate_index(self, v: int):
        if not isinstance(v, int):
            raise TypeError("vertex index must be int")
        if v < 0 or v >= self._n:
            raise IndexError(f"vertex index out of range: {v}")

    def _validate_edge_indices(self, u: int, v: int):
        self._validate_index(u)
        self._validate_index(v)

    # --- API ---
    def getVertexCount(self) -> int:
        return self._n

    def getEdgeCount(self) -> int:
        total = sum(len(s) for s in self._adj)
        return total if self.directed else total // 2

    def hasEdge(self, u: int, v: int) -> bool:
        self._validate_edge_indices(u, v)
        return v in self._adj[u]

    def addEdge(self, u: int, v: int):
        self._validate_edge_indices(u, v)
        if u == v:
            raise ValueError("loops are not allowed in simple graphs")
        if self.hasEdge(u, v):
            # idempotent: do nothing
            return
        # add edge
        self._adj[u].add(v)
        if not self.directed:
            self._adj[v].add(u)
        # default weight
        self._edge_weights[(u, v)] = self._edge_weights.get((u, v), 1.0)

    def removeEdge(self, u: int, v: int):
        self._validate_edge_indices(u, v)
        if not self.hasEdge(u, v):
            raise ValueError(f"edge ({u},{v}) does not exist")
        self._adj[u].remove(v)
        if not self.directed:
            self._adj[v].remove(u)
        self._edge_weights.pop((u, v), None)

    def isSucessor(self, u: int, v: int) -> bool:
        # v is successor of u <=> edge u->v exists
        return self.hasEdge(u, v)

    def isPredessor(self, u: int, v: int) -> bool:
        # v is predecessor of u <=> edge v->u exists
        self._validate_edge_indices(u, v)
        return self.hasEdge(v, u)

    def isDivergent(self, u1: int, v1: int, u2: int, v2: int) -> bool:
        # divergent: same source, different targets
        self._validate_edge_indices(u1, v1)
        self._validate_edge_indices(u2, v2)
        return u1 == u2 and v1 != v2

    def isConvergent(self, u1: int, v1: int, u2: int, v2: int) -> bool:
        # convergent: same target, different sources
        self._validate_edge_indices(u1, v1)
        self._validate_edge_indices(u2, v2)
        return v1 == v2 and u1 != u2

    def isIncident(self, u: int, v: int, x: int) -> bool:
        self._validate_edge_indices(u, v)
        self._validate_index(x)
        return x == u or x == v

    def getVertexInDegree(self, u: int) -> int:
        self._validate_index(u)
        if not self.directed:
            # undirected: in-degree == degree
            return len(self._adj[u])
        # directed: count predecessors
        cnt = 0
        for i in range(self._n):
            if u in self._adj[i]:
                cnt += 1
        return cnt

    def getVertexOutDegree(self, u: int) -> int:
        self._validate_index(u)
        return len(self._adj[u])

    def setVertexWeight(self, v: int, w: float):
        self._validate_index(v)
        self._vertex_weights[v] = float(w)

    def getVertexWeight(self, v: int) -> float:
        self._validate_index(v)
        return self._vertex_weights[v]

    def setEdgeWeight(self, u: int, v: int, w: float):
        if not self.hasEdge(u, v):
            raise ValueError(f"edge ({u},{v}) does not exist")
        self._edge_weights[(u, v)] = float(w)

    def getEdgeWeight(self, u: int, v: int) -> float:
        if not self.hasEdge(u, v):
            raise ValueError(f"edge ({u},{v}) does not exist")
        return self._edge_weights.get((u, v), 1.0)

    def isConnected(self) -> bool:
        # weak connectivity: treat graph as undirected
        if self._n == 0:
            return True
        visited = set()
        stack = [0]
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            # neighbors: outgoing
            for nb in self._adj[node]:
                if nb not in visited:
                    stack.append(nb)
            # neighbors: incoming
            for i in range(self._n):
                if node in self._adj[i] and i not in visited:
                    stack.append(i)
        return len(visited) == self._n

    def isEmptyGraph(self) -> bool:
        return self._n == 0

    def isCompleteGraph(self) -> bool:
        # complete (directed): every ordered pair u!=v has edge u->v
        for u in range(self._n):
            for v in range(self._n):
                if u == v:
                    continue
                if not self.hasEdge(u, v):
                    return False
        return True

    def exportToGEPHI(self, path: str):
        """Exporta o grafo para GEXF (aceito pelo Gephi) sem depender de bibliotecas externas.

        Implementação mínima do formato GEXF usando xml.etree.ElementTree da stdlib.
        Gera um arquivo que pode ser aberto pelo Gephi (nó id = inteiro, arestas com peso).
        """
        import xml.etree.ElementTree as ET

        NS = "http://www.gexf.net/1.2draft"
        xsi = "http://www.w3.org/2001/XMLSchema-instance"
        ET.register_namespace("", NS)
        ET.register_namespace("xsi", xsi)

        gexf = ET.Element("{http://www.gexf.net/1.2draft}gexf", {
            "version": "1.2"
        })
        graph_attribs = {
            "mode": "static",
            "defaultedgetype": "directed" if self.directed else "undirected",
        }
        graph = ET.SubElement(gexf, "graph", graph_attribs)

        # define node attribute for weight
        attributes = ET.SubElement(graph, "attributes", {"class": "node", "mode": "static"})
        ET.SubElement(attributes, "attribute", {"id": "0", "title": "weight", "type": "double"})

        nodes_el = ET.SubElement(graph, "nodes")
        for v in range(self._n):
            node = ET.SubElement(nodes_el, "node", {"id": str(v), "label": str(v)})
            attvalues = ET.SubElement(node, "attvalues")
            ET.SubElement(attvalues, "attvalue", {"for": "0", "value": str(self._vertex_weights[v])})

        edges_el = ET.SubElement(graph, "edges")
        eid = 0
        for u in range(self._n):
            for v in sorted(self._adj[u]):
                w = self._edge_weights.get((u, v), 1.0)
                ET.SubElement(edges_el, "edge", {
                    "id": str(eid),
                    "source": str(u),
                    "target": str(v),
                    "weight": str(w),
                })
                eid += 1

        tree = ET.ElementTree(gexf)
        # escrever arquivo com declaração XML
        tree.write(path, encoding="utf-8", xml_declaration=True)

    def __repr__(self) -> str:
        return f"Graph(n={self._n}, directed={self.directed}, edges={self.getEdgeCount()})"
