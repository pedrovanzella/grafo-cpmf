from __future__ import print_function


class Mardita:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def read_file(self, filename):
        with open(filename) as f:
            for line in f[1:]:
                l = line.rstrip()
                na, nb, val = l.split(" ")
                self.nodes[na] = True
                self.nodes[nb] = True
                self.edges[na + ',' + nb] = val

    def reduce_edges(self):
        pass


if __name__ == "__main__":
    print("hello")
