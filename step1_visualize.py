import multiprocessing

from pylab import *
from numpy import *

from sun2d_utils import *

i, j = loadtxt('inputs/ij.txt', dtype=int).T
xy = loadtxt('inputs/xy.txt')
x, y = xy[[i,j],0], xy[[i,j],1]

tris = construct_triangles(i, j)

seed(0)
colors = arange(8) / 8.

fname = 'outputs/parts.txt'
flags = loadhex(fname)
iproc = array(around(log2(flags)), int)
edges = []
for i, j, k in tris:
    xyc = (xy[i] + xy[j] + xy[k]) / 3
    if iproc[i] != iproc[j]:
        edges.append([(xy[i] + xy[j]) / 2, xyc])
    if iproc[j] != iproc[k]:
        edges.append([(xy[j] + xy[k]) / 2, xyc])
    if iproc[k] != iproc[i]:
        edges.append([(xy[k] + xy[i]) / 2, xyc])
x_e, y_e = transpose(edges, [2,1,0])

figure(figsize=(16,16))
plot(x_e, y_e, '0.5', zorder=0)
c = colors[iproc]
scatter(xy[:,0], xy[:,1], c=c, s=1, cmap='nipy_spectral',
        vmin=0, vmax=1, zorder=1)
colorbar()
axis('scaled')
axis('off')
title('Initial decomposition')
savefig('figs/initial.png')
