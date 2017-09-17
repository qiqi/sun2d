from numpy import *

def loadhex(fname):
    text = open(fname).read().replace('\n', '')
    return frombuffer(bytearray.fromhex(text), uint64).byteswap()

def construct_neighbors(i, j):
    n_nodes = array([i,j]).max() + 1
    neighbors = [set() for i in range(n_nodes)]
    for ii, jj in zip(i, j):
        neighbors[ii].add(jj)
        neighbors[jj].add(ii)
    return neighbors

def construct_triangles(i, j):
    neighbors = construct_neighbors(i, j)
    n_nodes = array([i,j]).max() + 1
    tris = set()
    for ii in range(n_nodes):
        for jj in neighbors[ii]:
            for kk in set.intersection(neighbors[ii], neighbors[jj]):
                tris.add(tuple(sorted([ii, jj, kk])))
    return tris

