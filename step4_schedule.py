import collections
from numpy import *

comm_cost = 10

flags, volume = loadtxt('outputs/volume.txt', dtype=int).T
volume_dict = {i: v for i, v in zip(flags, volume)}

flag_i, flag_j, area = loadtxt('outputs/connectivity.txt', dtype=int).T
area_dict = {(i,j) : a for i, j, a in zip(flag_i, flag_j, area)}

in_nodes = collections.defaultdict(set)
out_nodes = collections.defaultdict(set)
for i, j in zip(flag_i, flag_j):
    in_nodes[j].add(i)
    out_nodes[i].add(j)

print(len(flags), len(in_nodes), len(out_nodes))

level = {i: volume_dict[i] for i in flags}
active = set(flags).difference(set(out_nodes))
while active:
    j = active.pop()
    if j in in_nodes:
        for i in in_nodes[j]:
            edge_cost = area_dict[(i,j)] * comm_cost
            level[i] = max(level[i],
                           level[j] + edge_cost + volume_dict[i])
            active.add(i)

source = set(flags).difference(set(in_nodes))
source = sorted(source, key=lambda i : level[i], reverse=True)

