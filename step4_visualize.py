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

processor_assigned = {task: i for task, i in
        loadtxt('outputs/processor_assignment.txt', dtype=int)}

def visualize(i_level):
    print(i_level)
    cla()
    #plot(x, y, '0.5', zorder=0)

    fname_F = 'outputs/level_{:02d}.txt'.format(i_level)
    fname_B = 'outputs/level_{:02d}.txt'.format(32 - i_level)
    flags = left_shift(loadhex(fname_F), 8) + loadhex(fname_B)
    iproc = vectorize(processor_assigned.__getitem__)(flags)
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
    c = colors[iproc]
    scatter(xy[:,0], xy[:,1], c=c, s=1, cmap='nipy_spectral',
            vmin=0, vmax=1, zorder=1)
    #legend(['processor {}'.format(i) for i in range(8)], loc='upper left')
    plot(x_e, y_e, '0.5', zorder=0)
    axis('scaled')
    axis('off')
    title('level {}'.format(i_level))
    colorbar()
    savefig('figs/assignment_{:02d}.png'.format(i_level))
    close()

#for i in range(33):
#    visualize(i)
p = multiprocessing.Pool()
p.map(visualize, range(33))
