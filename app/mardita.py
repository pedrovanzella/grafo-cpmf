#!/usr/bin/env python

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
                val = self.get_edge(u, v)
                if val is not None:
                    graph.add_edge(u, v, label=val)

        return graph

    def get_edge(self, u, v):
        return self.edges.get(u + ',' + v, None)

    def remove_edge(self, u, v):
        edge = self.get_edge(u, v)
        if edge is not None:
            return self.edges.pop(u + ',' + v)

    def adjecent_nodes(self, a):
        nodes = []
        for u in self.nodes:
            if self.get_edge(a, u) is not None:
                nodes.append(u)

        return nodes

    def reduce_edges(self):
        for u in self.nodes:
            for v in self.adjecent_nodes(u):
                for a in self.adjecent_nodes(v):
                    # temos que verificar se temos saldo
                    if self.get_edge(v, a) < self.get_edge(u, v):
                        tmp = self.remove_edge(v, a)
                        self.edges[u + ',' + v] = tmp
                        if self.get_edge(u, a):
                            self.edges[u + ',' + a] += tmp
                        else:
                            self.edges[u + ',' + a] = tmp


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Uso: %s [arquivo]" % sys.argv[0])
        exit()

    m = Mardita()
    print("Reading file and creating graph")
    m.read_file(sys.argv[1])

    print("Writing graphiviz file")
    g = m.make_graph()
    g.write("../docs/" + sys.argv[1] + ".input.dot")

    print("Reducing edges")
    m.reduce_edges()

    print("Writing graphviz file of reduced edges")
    g = m.make_graph()
    g.write("../docs/" + sys.argv[1] + ".reduced.dot")
