import networkx

from decomposition_analysis import DecompositionAnalysis
from graphs import bipartite_graph_complete, complete_graph, undirected_graph


if __name__ == "__main__":
    # complete graph
    v = ['v_1', 'v_2', 'v_3', 'd']
    print(f"Checking complete graph (K_{len(v)}) ... ")
    decompositions = complete_graph(v)
    analysis = DecompositionAnalysis(decompositions)
    analysis.brute_force_decompositions()
    analysis.print_results()

    # complete bipartite graph
    a = ['a_1', 'a_2', 'a_3', 'd']
    b = ['b_1', 'b_2', 'b_3', 'b_4']
    print(f"Checking complete bipartite graph (K_({len(a)},{len(b)})) ... ")
    decompositions = bipartite_graph_complete(a, b)
    analysis = DecompositionAnalysis(decompositions)
    analysis.brute_force_decompositions()
    analysis.print_results()

    # special graph structure (joined cliques)
    a = networkx.complete_graph(['a_1', 'a_2', 'a_3'])
    b = networkx.complete_graph(['b_1', 'b_2', 'b_3'])
    print(f"Checking some special graph ...")
    joined_cliques = networkx.Graph(a)
    joined_cliques.add_edges_from(b.edges)
    joined_cliques.add_node('d')
    for node in joined_cliques.nodes:
        joined_cliques.add_edge('d', node)
    joined_cliques.remove_edge('d', 'd')
    decompositions = undirected_graph(joined_cliques, 3)
    analysis = DecompositionAnalysis(decompositions)
    analysis.brute_force_decompositions()
    analysis.print_results()
