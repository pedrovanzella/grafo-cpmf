#!/usr/bin/env python

from __future__ import print_function
import sys
import pygraphviz as pgv

DEBUG = False


class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, val):
        for n in self.nodes:
            if n.val == val:
                if DEBUG:
                    print("Added %r" % n)
                return n
        n = Graph.Node(val)
        self.nodes.append(n)
        return n

    @property
    def edges(self):
        edges = []
        for n in self.nodes:
            for e in n.edges:
                edges.append(e)
        return edges

    class Node:
        def __init__(self, val):
            self.val = val
            self.edges = []

        def add_edge(self, to, val):
            for e in self.edges:
                if e.to == to:
                    if DEBUG:
                        print("%r Already exists" % e)
                        # Se edge jah existe, aumenta o valor dela
                    return e.update_val(val)
            e = Graph.Edge(self, to, val)
            self.edges.append(e)
            if DEBUG:
                print("Added %r" % e)
            return e

        def remove_edge(self, edge):
            val = edge.val
            self.edges.remove(edge)
            if DEBUG:
                print("Remove %r" % edge)
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
                    if DEBUG:
                        print("Get Edge: %r -> %r: OK" % (self, v))
                    return e
            if DEBUG:
                print("Get Edge: %r -> %r: FAIL" % (self, v))
            return None

    class Edge:
        def __init__(self, fro, to, val):
            self.fro = fro
            self.to = to
            self.val = int(val)

        def update_val(self, val):
            if DEBUG:
                print("Old val: %r" % self)
            self.val += int(val)
            if DEBUG:
                print("New val: %r" % self)

        def __repr__(self):
            return "<Edge: (%r -> %r) = %d>" % (self.fro, self.to, self.val)


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
                a, b, val = l.split(" ")
                # create nodes
                na = self.graph.add_node(a)
                nb = self.graph.add_node(b)
                # create edge
                na.add_edge(nb, val)

    def make_graph(self):
        graph = pgv.AGraph(directed=True)
        for u in self.graph.nodes:
            graph.add_node(u.val)
            for v in u.adjecent_nodes:
                graph.add_edge(u.val, v.val, label=u.get_edge(v).val)

        return graph

    def total_tax_payed(self):
        total_transactions = 0
        for e in self.graph.edges:
            total_transactions += e.val
        return total_transactions * 0.01

    def reduce_edges(self):
        if DEBUG:
            count = 0
        # Tenho que fazer isto com lista e push pop
        for u in self.graph.nodes:
            vs = u.adjecent_nodes
            if DEBUG:
                print("adj(%r): %r" % (u, vs))
            while len(vs) > 0:
                v = vs.pop()
                for a in v.adjecent_nodes:
                    if DEBUG:
                        count += 1
                    if v.get_edge(a).val < u.get_edge(v).val:
                        tmp = v.get_edge(a).val
                        if DEBUG:
                            print("Removendo <v,a>")
                        v.remove_edge(v.get_edge(a))
                        u.get_edge(v).update_val(-tmp)
                        if u.get_edge(a) is not None:
                            u.get_edge(a).update_val(tmp)
                        else:
                            u.add_edge(a, tmp)
                            vs.append(a)
                    else:
                        if DEBUG:
                            print("Removendo <u,v>")
                        if v in vs:
                            vs.remove(v)
                        tmp = u.remove_edge(u.get_edge(v))
                        v.get_edge(a).update_val(-tmp)
                        u.add_edge(a, tmp)
                        vs.append(a)
                        break
        if DEBUG:
            print("Count: ", count)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Uso: %s [arquivo]" % sys.argv[0])
        exit()

    if len(sys.argv) == 3 and sys.argv[2] == 'DEBUG':
        DEBUG = True

    m = Mardita()
    if DEBUG:
        print("Reading file and creating graph")
    m.read_file(sys.argv[1])

    if DEBUG:
        print("Writing graphiviz file")
        g = m.make_graph()
        g.write("../docs/" + sys.argv[1] + ".input.dot")

    tax_before = m.total_tax_payed()
    if DEBUG:
        print("Total tax payed: ", tax_before)

    if DEBUG:
        print("Reducing edges")
    m.reduce_edges()

    if DEBUG:
        print("Writing graphviz file of reduced edges")
        g = m.make_graph()
        g.write("../docs/" + sys.argv[1] + ".reduced.dot")

    tax_after = m.total_tax_payed()
    if DEBUG:
        print("Total tax payed: ", tax_after)

    print("Total savings: ", tax_before - tax_after)
