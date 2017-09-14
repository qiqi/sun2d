from numpy import *

import networkx
import metis

ij = loadtxt('inputs/ij.txt', dtype=int)

n_part = 8
G = networkx.Graph()
G.add_nodes_from(arange(ij.max() + 1))
G.add_edges_from(ij)
edgecuts, parts = metis.part_graph(G, n_part, contig=True)
parts = array(parts, uint64)

assert n_part <= 64
flag = left_shift(ones(len(parts), dtype=uint64), parts)
savetxt('outputs/parts.txt', flag[:,newaxis], fmt='%016X')
