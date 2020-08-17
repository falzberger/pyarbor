from more_itertools import flatten
from typing import *
import networkx as nx


def find_incident_edge(graph: nx.DiGraph, edges: Set[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    """
    Given a nx.DiGraph G and a set of directed edges, returns the first edge e = (u,v) s.t. u is in G and v is not.
    If no such edge is found, returns None.

    :param graph: nx.DiGraph
    :param edges: Set of edges (integer tuples)
    :return: an edge e = (u, v) or None
    """
    for e in edges:
        if e[0] in graph.nodes and e[1] not in graph.nodes:
            return e
    return None


def tarjan_condition(edge: Tuple[int, int], graph: nx.DiGraph, edges_used: Set[Tuple[int, int]],
                     connectivity: int, destination: str) -> bool:
    """
    Checks the condition for arborescence decomposition construction according to Tarjan (1974).
    :param edge: the edge for which the condition should be checked
    :param graph: the original graph of the arborescence decomposition
    :param edges_used: all edges used for arborescences up to this point
    :param connectivity: the desired connectivity, i.e. the number of arborescences that still need to be constructed
    :param destination: the destination vertex of the decomposition
    :return: a boolean, indicating if the condition is fulfilled
    """
    if connectivity == 0:
        return True

    reduced_graph = graph.copy()
    reduced_graph.remove_edges_from(edges_used)
    reduced_graph.remove_edge(edge[0], edge[1])  # TODO: not mentioned in Tarjan?

    for i in range(1, connectivity + 1):
        reduced_graph.add_edge(edge[0], f"helper_node_{i}")
        reduced_graph.add_edge(f"helper_node_{i}", destination)

    return nx.edge_connectivity(reduced_graph, edge[0], edge[1]) >= connectivity


def adbed_decomposition(graph: nx.DiGraph, connectivity: int, destination: str):
    decomposition = []
    edges_odd = set()
    edges_even = set()

    for j in range(1, connectivity + 1):
        print(f"constructing arborescence {j}")
        arborescence = nx.DiGraph()
        arborescence.add_node(destination)

        edges_used = set(flatten(map(lambda arb: arb.edges, decomposition)))
        edges_usable = set(graph.edges).difference(edges_used)

        if j % 2 == 1 and j != k:
            edges_usable.difference_update(edges_even)
        elif j % 2 == 0:
            edges_usable.difference_update(edges_odd)

        edges_visited = []
        while len(arborescence.nodes) != len(graph.nodes):
            edges_priority = edges_odd if j % 2 == 1 else edges_even
            edges_priority = edges_priority.copy().intersection(edges_usable)
            e = find_incident_edge(arborescence, edges_priority)

            if e is None:
                e = find_incident_edge(arborescence, edges_usable)
                assert e is not None

            edges_visited.append(e)
            edges_usable.remove(e)

            if tarjan_condition(e, graph, edges_used, connectivity - j, destination):
                arborescence.add_edge(e[0], e[1])
                edges_used.add(e)
                edges_odd.discard(e) if j % 2 == 1 else edges_even.discard(e)

                e_reverse = (e[1], e[0])
                if e_reverse not in edges_used:
                    edges_even.add(e_reverse) if j % 2 == 1 else edges_odd.add(e_reverse)

        decomposition.append(arborescence)

    reversed_decomposition = map(lambda arb: arb.reverse(), decomposition)
    return reversed_decomposition


if __name__ == '__main__':
    g: nx.DiGraph = nx.read_adjlist(f"graphs/hog/graph_234.lst", delimiter=" ")
    g = g.to_directed()
    k = nx.edge_connectivity(g)
    print(f"given graph is {k}-edge-connected")
    adbed_decomposition(g, k, destination='1')
