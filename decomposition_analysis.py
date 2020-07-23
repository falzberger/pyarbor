import networkx

from typing import *

from arborescence_decomposition import ArborescenceDecomposition, brute_force_decomposition


class DecompositionAnalysis:

    def __init__(self, decompositions: List[Tuple[ArborescenceDecomposition, networkx.DiGraph]]) -> None:
        self.decompositions: List[Tuple[ArborescenceDecomposition, networkx.DiGraph]] = decompositions
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

        n_shared = len([a for a in self.complete_decompositions if a.is_c_shared(2)])
        print(f"The graph has {n_shared} 2-shared arborescence decompositions.")
        # TODO: do something intelligent here

    def print_results(self):
        if len(self.complete_decompositions) == 0:
            print("Could not find any valid arborescence decomposition")
        else:
            self.analyse_results()
        #     for decomposition in self.complete_decompositions:
        #         print("=== DECOMPOSITION ===")
        #         for arborescence in decomposition:
        #             print(arborescence)
        #         print()
        print(f"Found {len(self.complete_decompositions)} decompositions in total.")
