import collections

from numpy import *
from scipy import  sparse

from sun2d_utils import *

nodes = collections.defaultdict(int)

i, j = loadtxt('inputs/ij.txt', dtype=int).T

connectivity = ([], [])

prev_flags = None
for i_level in range(33):
    fname = 'outputs/level_{:02d}.txt'.format(i_level)
    flags_F = loadhex(fname)
    fname = 'outputs/level_{:02d}.txt'.format(32-i_level)
    flags_B = loadhex(fname)
    flags = left_shift(flags_F, 8) + flags_B
    for flag, count in zip(*unique(flags, return_counts=True)):
        nodes[flag] += count

    if prev_flags is not None:
        connectivity[0].extend(list(prev_flags[i]))
        connectivity[1].extend(list(flags[j]))
    prev_flags = flags

savetxt('outputs/volume.txt', list(nodes.items()), fmt='%d')

A = sparse.csr_matrix((ones(len(connectivity[0])), connectivity))
savetxt('outputs/connectivity.txt', transpose(sparse.find(A)), fmt='%d')
