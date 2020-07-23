import itertools
import networkx

from typing import *
from arborescence import Arborescence, brute_force_decomposition


def _init_arborescences(graph: networkx.DiGraph, edge_connectivity: int) -> List[
    Tuple[List[Arborescence], networkx.DiGraph]]:
    assert 'd' in graph

    init_arcs = [(v, 'd') for v in graph.neighbors('d') if v != 'd']
    arborescence_decompositions = []
    for arc_combination in itertools.combinations(init_arcs, edge_connectivity):
        arborescences = []
        for arc in arc_combination:
            arborescence = Arborescence()
            arborescence.add_arc(arc[0], arc[1])
            arborescences.append(arborescence)

        reduced_graph = graph.copy()
        reduced_graph.remove_edges_from(arc_combination)
        arborescence_decompositions.append((arborescences, reduced_graph))

    return arborescence_decompositions


def bipartite_graph_complete(a: List[AnyStr], b: List[AnyStr]) -> List[Tuple[List[Arborescence], networkx.DiGraph]]:
    graph = networkx.complete_multipartite_graph(a, b)
    connectivity = min([len(a), len(b)])
    return undirected_graph(graph, connectivity)


def complete_graph(vertices: List[AnyStr]) -> List[Tuple[List[Arborescence], networkx.DiGraph]]:
    graph = networkx.complete_graph(vertices)
    return undirected_graph(graph, edge_connectivity=(len(graph) - 1))


def undirected_graph(graph: networkx.Graph, edge_connectivity: int) -> List[
    Tuple[List[Arborescence], networkx.DiGraph]]:
    assert 'd' in graph
    decompositions = _init_arborescences(graph.to_directed(), edge_connectivity)
    print(f"Found {len(decompositions)} distinct starting arborescence combination(s).")
    return decompositions
