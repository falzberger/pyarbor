import networkx as nx


class Arborescence:

    def __init__(self, graph: nx.DiGraph = None) -> None:
        if graph is None:
            graph = nx.DiGraph()
            graph.add_node('d')

        self.graph = nx.DiGraph(graph)

    def __copy__(self):
        return Arborescence(self.graph.copy())

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
        self.graph.add_edge(u, v)

    def add_arcs(self, arcs: [(str, str)]) -> None:
        for arc in arcs:
            self.add_arc(arc[0], arc[1])

    def has_arc(self, u: str, v: str) -> bool:
        return self.graph.has_edge(u, v)

    def has_vertex(self, v: str) -> bool:
        return v in self.graph

    def shares_links(self, other) -> bool:
        induced_subgraph = self.graph.to_undirected().edge_subgraph(other.arcs)
        return len(induced_subgraph.edges) > 0
