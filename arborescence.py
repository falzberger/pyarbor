import itertools
import networkx as nx

from copy import copy
from typing import *


class Arborescence:

    def __init__(self, graph: nx.DiGraph = None, leaves=None) -> None:
        if graph is None:
            graph = nx.DiGraph()
            graph.add_node('d')
        if leaves is None:
            leaves = ['d']

        self.graph = nx.DiGraph(graph)
        self.leaves = set(leaves)  # convenience variable that contains all vertices with no incident arcs

    def __copy__(self):
        return Arborescence(self.graph.copy(), self.leaves)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Arborescence):
            return self.graph == o.graph
        return False

    def __str__(self) -> str:
        return f"Arborescence: arcs:{self.arcs} vertices:{self.vertices}"

    @property
    def arcs(self):
        return self.graph.edges

    @property
    def vertices(self):
        return self.graph.nodes

    def add_arc(self, u: str, v: str) -> None:
        assert v in self.graph
        if v in self.leaves:
            self.leaves.remove(v)

        self.graph.add_edge(u, v)
        self.leaves.add(u)

    def add_arcs(self, arcs: [(str, str)]) -> None:
        for arc in arcs:
            self.add_arc(arc[0], arc[1])

    def has_arc(self, u: str, v: str) -> bool:
        return self.graph.has_edge(u, v)

    def has_vertex(self, v: str) -> bool:
        return v in self.graph

    def shares_links(self, other) -> bool:
        return any(arc in self.arcs or self.graph.has_edge(arc[1], arc[0]) for arc in other.arcs)
        # for arc in other.arcs:
        #     if arc in self.arcs or (arc[1], arc[0]) in self.arcs:
        #         return True


def brute_force_decomposition(arborescence_stubs: List[Arborescence], graph: nx.DiGraph) -> List[List[Arborescence]]:
    """
    Takes a set of initial arborescences and returns a brute-forced list of all possible arborescence decompositions.
    :param arborescence_stubs: the initial set of Arborescence objects (initialized with an arc to the destination)
    :param graph:
    :return: a list of lists, each representing a possible arborescence decomposition
    """
    assert len(arborescence_stubs) > 0
    try:
        arborescence = next(a for a in arborescence_stubs if len(a.vertices) < len(graph))
    except StopIteration:
        # print("Found an arc-disjoint arborescence decomposition.")
        return [arborescence_stubs]

    variants = brute_force_arborescence(arborescence, graph)
    # print(f"Found {len(variants)} variants for arborescence-stub number {arborescence_stubs.index(arborescence)}.")

    decompositions = []
    for variant in variants:
        # print(f"found arborescence: {variant}")
        # print(f"doing next arborescence with ars: {arcs}")
        reduced_graph = graph.copy()
        reduced_graph.remove_edges_from(variant.arcs)
        decompositions.extend(
            # replace the stub with the complete arborescence and recursively call procedure again
            brute_force_decomposition([variant if a == arborescence else a for a in arborescence_stubs], reduced_graph))
    return decompositions


def brute_force_arborescence(arborescence_stub: Arborescence, graph: nx.DiGraph) -> List[Arborescence]:
    """
    Creates all possible arborescences on basis of the given arborescence and the available set of arcs in the graph.
    :param arborescence_stub: the initial Arborescence stub on which to create all possible arborescences
    :param graph:
    :return: a set of all possible arborescences
    """
    assert len(arborescence_stub.vertices) > 1 and not len(arborescence_stub.vertices) > len(graph)
    # print(f"filling the following arborescence: {arborescence_stub}")

    if len(arborescence_stub.vertices) == len(graph):
        if len(arborescence_stub.arcs) != len(graph) - 1:  # fundamental property of trees
            return []
        else:
            return [arborescence_stub]

    else:
        candidate_arcs = [arc for arc in graph.edges if
                          arc[0] not in arborescence_stub.vertices and arc[1] in arborescence_stub.vertices]
        if len(candidate_arcs) == 0:
            return []
        powerset = list(itertools.chain.from_iterable(
            itertools.combinations(candidate_arcs, r) for r in range(1, len(candidate_arcs) + 1, 1)))

        # Only sets that add a vertex exactly one time are valid candidates
        candidates = []
        for candidate_set in powerset:
            incident_vertices = set()
            valid = True
            for arc in candidate_set:
                if arc[0] in incident_vertices:
                    # print(f"removing the candidate: {candidate_set}")
                    valid = False
                    break
                incident_vertices.add(arc[0])
            if valid:
                candidates.append(candidate_set)

        # print(f"{len(candidates)} possible arc-combinations for the next step.")
        results = []
        for candidate_set in candidates:
            arborescence = copy(arborescence_stub)
            arborescence.add_arcs(candidate_set)
            # reduced_arcs = [arc for arc in arcs if arc not in candidate_set]
            # print(f"current candidate set: {candidate_set}")
            # print(f"one step deeper with arcs: {reduced_arcs}")
            reduced_graph = graph.copy()
            reduced_graph.remove_edges_from(candidate_arcs)
            results.extend(brute_force_arborescence(arborescence, reduced_graph))

        return results
