#!/usr/bin/env python

from __future__ import print_function
import sys
import pygraphviz as pgv


class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, val):
        n = Graph.Node(val)
        self.nodes.append(n)
        return n

    class Node:
        def __init__(self, val):
            self.val = val
            self.edges = []

        def add_edge(self, to, val):
            e = Graph.Edge(self, to, val)
            self.edges.append(e)
            return e

        def remove_edge(self, edge):
            self.edges.remove(edge)

    class Edge:
        def __init__(self, fro, to, val):
            self.fro = fro
            self.to = to
            self.val = val

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
            return int(self.edges.pop(u + ',' + v))

    def adjecent_nodes(self, a):
        # Temos que retornar com _next_ e afins
        # para atualizar a lista sempre
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
                    if self.get_edge(v, a) <= self.get_edge(u, v):
                        # remove esta aresta
                        tmp = self.remove_edge(v, a)
                        self.edges[u + ',' + v] -= tmp
                        if self.get_edge(u, a):
                            # Se a aresta jah existe, aumenta o valor
                            self.edges[u + ',' + a] += tmp
                        else:
                            # Senao, cria ela
                            # quando eu crio esta aresta, o iterador nao eh
                            # alterado
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
