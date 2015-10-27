from __future__ import print_function
import sys
import pygraphviz as pgv


class Mardita:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def read_file(self, filename):
        with open(filename) as f:
            # Skip the first line
            for line in f.readlines()[1:]:
                # strip trailing spaces
                l = line.rstrip()
                # split on spaces
                na, nb, val = l.split(" ")
                # create nodes
                self.nodes[na] = True
                self.nodes[nb] = True
                # create edges
                self.edges[na + ',' + nb] = val

    def make_graph(self):
        graph = pgv.AGraph(directed=True)
        for u in self.nodes:
            graph.add_node(u)
            for v in self.nodes:
                if self.edges.get(u + ',' + v, None) is not None:
                    graph.add_edge(u, v, label=self.edges[u + ',' + v])

        return graph

    def reduce_edges(self):
        pass


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Uso: %s [arquivo]" % sys.argv[0])
        exit()

    m = Mardita()
    m.read_file(sys.argv[1])
    g = m.make_graph()
    g.write("../docs/" + sys.argv[1] + ".input.dot")
