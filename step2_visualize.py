import multiprocessing

from pylab import *
from numpy import *

from sun2d_utils import *

i, j = loadtxt('inputs/ij.txt', dtype=int).T
xy = loadtxt('inputs/xy.txt')
x, y = xy[[i,j],0], xy[[i,j],1]

tris = construct_triangles(i, j)

seed(0)
colors = rand(2**16)

def visualize(i_level):
    print(i_level)
    cla()
    #plot(x, y, '0.5', zorder=0)

    fname = 'outputs/level_{:02d}.txt'.format(i_level)
    flags = loadhex(fname)
    edges = []
    for i, j, k in tris:
        xyc = (xy[i] + xy[j] + xy[k]) / 3
        if flags[i] != flags[j]:
            edges.append([(xy[i] + xy[j]) / 2, xyc])
        if flags[j] != flags[k]:
            edges.append([(xy[j] + xy[k]) / 2, xyc])
        if flags[k] != flags[i]:
            edges.append([(xy[k] + xy[i]) / 2, xyc])
    x_e, y_e = transpose(edges, [2,1,0])

    figure(figsize=(16,16))
    plot(x_e, y_e, '-r', zorder=2)
    flags_F = flags.copy()

    fname = 'outputs/level_{:02d}.txt'.format(32-i_level)
    flags = loadhex(fname)
    edges = []
    for i, j, k in tris:
        xyc = (xy[i] + xy[j] + xy[k]) / 3
        if flags[i] != flags[j]:
            edges.append([(xy[i] + xy[j]) / 2, xyc])
        if flags[j] != flags[k]:
            edges.append([(xy[j] + xy[k]) / 2, xyc])
        if flags[k] != flags[i]:
            edges.append([(xy[k] + xy[i]) / 2, xyc])
    x_e, y_e = transpose(edges, [2,1,0])
    plot(x_e, y_e, '-g', zorder=2)
    flags_B = flags.copy()

    c = colors[left_shift(flags_F, 8) + flags_B]
    scatter(xy[:,0], xy[:,1], c=c, s=1, cmap='nipy_spectral',
            vmin=0, vmax=1, zorder=1)
    axis('scaled')
    axis('off')
    title('level {}'.format(i_level))
    savefig('figs/level_{:02d}.png'.format(i_level))

p = multiprocessing.Pool()
p.map(visualize, range(33))
