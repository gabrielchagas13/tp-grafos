from typing import Iterable, List, Set, Tuple
from .abstract_graph import AbstractGraph


class AdjacencyListGraph(AbstractGraph):
    def __init__(self, num_vertices: int, directed: bool = True):
        super().__init__(num_vertices, directed=directed)
        self._adj: List[Set[int]] = [set() for _ in range(self._n)]

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
            return
        self._adj[u].add(v)
        if not self.directed:
            self._adj[v].add(u)
        # default edge weight
        self._edge_weights[(u, v)] = self._edge_weights.get((u, v), 1.0)

    def removeEdge(self, u: int, v: int):
        self._validate_edge_indices(u, v)
        if not self.hasEdge(u, v):
            raise ValueError(f"edge ({u},{v}) does not exist")
        self._adj[u].remove(v)
        if not self.directed:
            self._adj[v].remove(u)
        self._edge_weights.pop((u, v), None)

    def getVertexOutDegree(self, u: int) -> int:
        self._validate_index(u)
        return len(self._adj[u])

    def getOutgoing(self, u: int) -> Iterable[int]:
        self._validate_index(u)
        return iter(self._adj[u])

    def getAllEdges(self) -> Iterable[Tuple[int, int]]:
        for u in range(self._n):
            for v in sorted(self._adj[u]):
                yield (u, v)

    def __repr__(self) -> str:
        return f"AdjacencyListGraph(n={self._n}, directed={self.directed}, edges={self.getEdgeCount()})"
