#!/usr/bin/env python

from __future__ import print_function
import sys
import pygraphviz as pgv


class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, val):
        for n in self.nodes:
            if n.val == val:
                return n
        n = Graph.Node(val)
        self.nodes.append(n)
        return n

    class Node:
        def __init__(self, val):
            self.val = val
            self.edges = []

        def add_edge(self, to, val):
            # THIS IS WRONG
            e = Graph.Edge(self, to, val)
            self.edges.append(e)
            return e

        def remove_edge(self, edge):
            val = edge.val
            self.edges.remove(edge)
            return val

        def __repr__(self):
            return "<Node %s>" % self.val

        @property
        def adjecent_nodes(self):
            nodes = []
            for e in self.edges:
                if e.to not in nodes:
                    nodes.append(e.to)
            return nodes

        def get_edge(self, v):
            for e in self.edges:
                if e.to == v:
                    return e
            return None

    class Edge:
        def __init__(self, fro, to, val):
            self.fro = fro
            self.to = to
            self.val = int(val)

        def update_val(self, val):
            self.val += val


class Mardita:
    def __init__(self):
        self.graph = Graph()

    def read_file(self, filename):
        with open(filename) as f:
            # Skip the first line
            for line in f.readlines()[1:]:
                # strip trailing spaces
                l = line.rstrip()
                # split on spaces
                na, nb, val = l.split(" ")
                # create nodes
                nan = self.graph.add_node(na)
                nbn = self.graph.add_node(nb)
                # create edge
                nan.add_edge(nbn, val)

    def make_graph(self):
        graph = pgv.AGraph(directed=True)
        for u in self.graph.nodes:
            graph.add_node(u.val)
            for e in u.edges:
                graph.add_edge(u.val, e.to.val, label=e.val)

        return graph

    def reduce_edges(self):
        for u in self.graph.nodes:
            print("adj(%r): %r" % (u, u.adjecent_nodes))
            for v in u.adjecent_nodes:
                for a in v.adjecent_nodes:
                    if v.get_edge(a).val < u.get_edge(v).val:
                        tmp = v.get_edge(a).val
                        v.remove_edge(v.get_edge(a))
                        u.get_edge(v).update_val(-tmp)
                        if u.get_edge(a) is not None:
                            u.get_edge(a).update_val(tmp)
                        else:
                            u.add_edge(a, tmp)


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
