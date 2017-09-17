import collections

from numpy import *
from scipy import  sparse

from sun2d_utils import *

def load_flags(i_level):
    fname = 'outputs/level_{:02d}.txt'.format(i_level)
    flags_F = loadhex(fname)
    fname = 'outputs/level_{:02d}.txt'.format(32-i_level)
    flags_B = loadhex(fname)
    return left_shift(flags_F, 8) + flags_B

nodes = collections.defaultdict(int)

i, j = loadtxt('inputs/ij.txt', dtype=int).T

connectivity = ([], [])

flags = load_flags(0)
for flag, count in zip(*unique(flags, return_counts=True)):
    start_flag = flag & uint64(255 * 256)
    nodes[start_flag] = 0
    nodes[flag] += count
    connectivity[0].extend([start_flag] * count)
    connectivity[1].extend([flag] * count)

prev_flags = flags
for i_level in range(1, 33):
    flags = load_flags(i_level)
    for flag, count in zip(*unique(flags, return_counts=True)):
        nodes[flag] += count

    if prev_flags is not None:
        connectivity[0].extend(list(prev_flags[i]))
        connectivity[1].extend(list(flags[j]))
    prev_flags = flags

for flag, count in zip(*unique(flags, return_counts=True)):
    final_flag = flag & uint64(255)
    nodes[final_flag] = 0
    connectivity[0].extend([flag] * count)
    connectivity[1].extend([final_flag] * count)

savetxt('outputs/volume.txt', list(nodes.items()), fmt='%d')

A = sparse.csr_matrix((ones(len(connectivity[0])), connectivity))
A.setdiag(0)
savetxt('outputs/connectivity.txt', transpose(sparse.find(A)), fmt='%d')
