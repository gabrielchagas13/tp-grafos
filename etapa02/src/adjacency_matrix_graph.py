from typing import Iterable, Tuple
from .abstract_graph import AbstractGraph


class AdjacencyMatrixGraph(AbstractGraph):
    def __init__(self, num_vertices: int, directed: bool = True):
        super().__init__(num_vertices, directed=directed)
        # adjacency matrix of booleans
        self._mat = [[False for _ in range(self._n)] for _ in range(self._n)]

    def getVertexCount(self) -> int:
        return self._n

    def getEdgeCount(self) -> int:
        total = 0
        for u in range(self._n):
            for v in range(self._n):
                if self._mat[u][v]:
                    total += 1
        return total if self.directed else total // 2

    def hasEdge(self, u: int, v: int) -> bool:
        self._validate_edge_indices(u, v)
        return bool(self._mat[u][v])

    def addEdge(self, u: int, v: int):
        self._validate_edge_indices(u, v)
        if u == v:
            raise ValueError("loops are not allowed in simple graphs")
        if self._mat[u][v]:
            return
        self._mat[u][v] = True
        if not self.directed:
            self._mat[v][u] = True
        self._edge_weights[(u, v)] = self._edge_weights.get((u, v), 1.0)

    def removeEdge(self, u: int, v: int):
        self._validate_edge_indices(u, v)
        if not self._mat[u][v]:
            raise ValueError(f"edge ({u},{v}) does not exist")
        self._mat[u][v] = False
        if not self.directed:
            self._mat[v][u] = False
        self._edge_weights.pop((u, v), None)

    def getVertexOutDegree(self, u: int) -> int:
        self._validate_index(u)
        return sum(1 for v in range(self._n) if self._mat[u][v])

    def getOutgoing(self, u: int) -> Iterable[int]:
        self._validate_index(u)
        for v in range(self._n):
            if self._mat[u][v]:
                yield v

    def getAllEdges(self) -> Iterable[Tuple[int, int]]:
        for u in range(self._n):
            for v in range(self._n):
                if self._mat[u][v]:
                    yield (u, v)

    def __repr__(self) -> str:
        return f"AdjacencyMatrixGraph(n={self._n}, directed={self.directed}, edges={self.getEdgeCount()})"
