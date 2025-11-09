import os
import sys
import tempfile

# allow importing from project root (so `from src.graph import Graph` works)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pytest

from src.adjacency_list_graph import AdjacencyListGraph
from src.adjacency_matrix_graph import AdjacencyMatrixGraph


@pytest.mark.parametrize("GraphClass", [AdjacencyListGraph, AdjacencyMatrixGraph])
def test_basic_add_and_counts(GraphClass):
    g = GraphClass(3, directed=True)
    assert g.getVertexCount() == 3
    assert g.getEdgeCount() == 0
    g.addEdge(0, 1)
    assert g.hasEdge(0, 1)
    assert g.getEdgeCount() == 1
    # idempotent
    g.addEdge(0, 1)
    assert g.getEdgeCount() == 1


@pytest.mark.parametrize("GraphClass", [AdjacencyListGraph, AdjacencyMatrixGraph])
def test_no_loops_and_invalid_index(GraphClass):
    g = GraphClass(2)
    with pytest.raises(ValueError):
        g.addEdge(0, 0)
    with pytest.raises(IndexError):
        g.addEdge(-1, 1)
    with pytest.raises(IndexError):
        g.hasEdge(0, 5)


@pytest.mark.parametrize("GraphClass", [AdjacencyListGraph, AdjacencyMatrixGraph])
def test_degrees_and_incident(GraphClass):
    g = GraphClass(4, directed=True)
    g.addEdge(0, 1)
    g.addEdge(0, 2)
    g.addEdge(2, 1)
    assert g.getVertexOutDegree(0) == 2
    assert g.getVertexInDegree(1) == 2
    assert g.isDivergent(0, 1, 0, 2)
    assert g.isConvergent(0, 1, 2, 1)
    assert g.isIncident(0, 1, 1)


@pytest.mark.parametrize("GraphClass", [AdjacencyListGraph, AdjacencyMatrixGraph])
def test_weights_and_remove(GraphClass):
    g = GraphClass(3)
    g.addEdge(0, 1)
    g.setEdgeWeight(0, 1, 3.14)
    assert abs(g.getEdgeWeight(0, 1) - 3.14) < 1e-9
    g.setVertexWeight(2, 2.5)
    assert abs(g.getVertexWeight(2) - 2.5) < 1e-9
    g.removeEdge(0, 1)
    with pytest.raises(ValueError):
        g.getEdgeWeight(0, 1)


@pytest.mark.parametrize("GraphClass", [AdjacencyListGraph, AdjacencyMatrixGraph])
def test_export_to_gephi(GraphClass, tmp_path):
    g = GraphClass(3, directed=True)
    g.addEdge(0, 1)
    g.addEdge(1, 2)
    out = tmp_path / "test_out.gexf"
    g.exportToGEPHI(str(out))
    assert out.exists()
