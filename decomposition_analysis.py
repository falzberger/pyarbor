import networkx

from typing import *

from arborescence import Arborescence, brute_force_decomposition


class DecompositionAnalysis:

    def __init__(self, decompositions: List[Tuple[List[Arborescence], networkx.DiGraph]]) -> None:
        self.decompositions: List[Tuple[List[Arborescence], networkx.DiGraph]] = decompositions
        self.complete_decompositions = []

    def brute_force_decompositions(self):
        for decomposition, graph in self.decompositions:
            print(f"Trying next decomposition with remaining arcs: {graph.edges}")
            finished_decompositions = brute_force_decomposition(decomposition, graph)
            self.complete_decompositions.extend(finished_decompositions)

    def analyse_results(self):
        if len(self.complete_decompositions) == 0:
            print("There aren't any valid arborescence decompositions")
            return
        # TODO: do something intelligent here

    def print_results(self):
        if len(self.complete_decompositions) == 0:
            print("Could not find any valid arborescence decomposition")
        # else:
        #     for decomposition in self.complete_decompositions:
        #         print("=== DECOMPOSITION ===")
        #         for arborescence in decomposition:
        #             print(arborescence)
        #         print()
        print(f"Found {len(self.complete_decompositions)} decompositions in total.")
