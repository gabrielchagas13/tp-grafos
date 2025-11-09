from abc import ABC, abstractmethod
from typing import Iterable, Tuple


class AbstractGraph(ABC):
    def __init__(self, num_vertices: int, directed: bool = True):
        if num_vertices < 0:
            raise ValueError("num_vertices must be non-negative")
        self._n = int(num_vertices)
        self.directed = bool(directed)
        # vertex weights and edge weights stored in base class
        self._vertex_weights = [0.0 for _ in range(self._n)]
        # edge weights stored as (u,v) -> float
        self._edge_weights = {}

    # --- abstract primitives children must implement ---
    @abstractmethod
    def getVertexCount(self) -> int:
        pass

    @abstractmethod
    def getEdgeCount(self) -> int:
        pass

    @abstractmethod
    def hasEdge(self, u: int, v: int) -> bool:
        pass

    @abstractmethod
    def addEdge(self, u: int, v: int):
        pass

    @abstractmethod
    def removeEdge(self, u: int, v: int):
        pass

    @abstractmethod
    def getVertexOutDegree(self, u: int) -> int:
        pass

    @abstractmethod
    def getOutgoing(self, u: int) -> Iterable[int]:
        """Retorna os vizinhos de saída de u (iterável)."""
        pass

    @abstractmethod
    def getAllEdges(self) -> Iterable[Tuple[int, int]]:
        """Retorna todos os pares de arestas (u,v)."""
        pass

    # --- helpers ---
    def _validate_index(self, v: int):
        if not isinstance(v, int):
            raise TypeError("vertex index must be int")
        if v < 0 or v >= self._n:
            raise IndexError(f"vertex index out of range: {v}")

    def _validate_edge_indices(self, u: int, v: int):
        self._validate_index(u)
        self._validate_index(v)

    # --- default implementations using primitives ---
    def isSucessor(self, u: int, v: int) -> bool:
        return self.hasEdge(u, v)

    def isPredessor(self, u: int, v: int) -> bool:
        self._validate_edge_indices(u, v)
        return self.hasEdge(v, u)

    def isDivergent(self, u1: int, v1: int, u2: int, v2: int) -> bool:
        self._validate_edge_indices(u1, v1)
        self._validate_edge_indices(u2, v2)
        return u1 == u2 and v1 != v2

    def isConvergent(self, u1: int, v1: int, u2: int, v2: int) -> bool:
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
            return self.getVertexOutDegree(u)
        cnt = 0
        for a, b in self.getAllEdges():
            if b == u:
                cnt += 1
        return cnt

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
        # weak connectivity: treat as undirected
        if self._n == 0:
            return True
        visited = set()
        stack = [0]
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            # outgoing
            for nb in self.getOutgoing(node):
                if nb not in visited:
                    stack.append(nb)
            # incoming: scan all edges for predecessors
            for a, b in self.getAllEdges():
                if b == node and a not in visited:
                    stack.append(a)
        return len(visited) == self._n

    def isEmptyGraph(self) -> bool:
        return self._n == 0

    def isCompleteGraph(self) -> bool:
        for u in range(self._n):
            for v in range(self._n):
                if u == v:
                    continue
                if not self.hasEdge(u, v):
                    return False
        return True

    def exportToGEPHI(self, path: str):
        # implement GEXF export using stdlib XML
        import xml.etree.ElementTree as ET

        NS = "http://www.gexf.net/1.2draft"
        xsi = "http://www.w3.org/2001/XMLSchema-instance"
        ET.register_namespace("", NS)
        ET.register_namespace("xsi", xsi)

        gexf = ET.Element("{http://www.gexf.net/1.2draft}gexf", {"version": "1.2"})
        graph_attribs = {"mode": "static", "defaultedgetype": "directed" if self.directed else "undirected"}
        graph = ET.SubElement(gexf, "graph", graph_attribs)

        attributes = ET.SubElement(graph, "attributes", {"class": "node", "mode": "static"})
        ET.SubElement(attributes, "attribute", {"id": "0", "title": "weight", "type": "double"})

        nodes_el = ET.SubElement(graph, "nodes")
        for v in range(self._n):
            node = ET.SubElement(nodes_el, "node", {"id": str(v), "label": str(v)})
            attvalues = ET.SubElement(node, "attvalues")
            ET.SubElement(attvalues, "attvalue", {"for": "0", "value": str(self._vertex_weights[v])})

        edges_el = ET.SubElement(graph, "edges")
        eid = 0
        for u, v in self.getAllEdges():
            w = self._edge_weights.get((u, v), 1.0)
            ET.SubElement(edges_el, "edge", {"id": str(eid), "source": str(u), "target": str(v), "weight": str(w)})
            eid += 1

        tree = ET.ElementTree(gexf)
        tree.write(path, encoding="utf-8", xml_declaration=True)
