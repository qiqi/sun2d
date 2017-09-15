import matplotlib
from pylab import *
from numpy import *

seed(0)
colors = rand(2**16)
cmap = matplotlib.cm.get_cmap('nipy_spectral')

with open('outputs/dependency.dot', 'wt') as fh:
    fh.write('digraph {\n')
    volume = loadtxt('outputs/volume.txt', dtype=int)
    vmax = float(volume[:,-1].max())
    for flag, v in volume:
        color = matplotlib.colors.rgb2hex(cmap(colors[flag])[:3])
        fh.write('{0} [width={1}, height={1},'.format(flag, sqrt(v / vmax)))
        fh.write('color="{}",'.format(color))
        fh.write('fixedsize=true, label="", style="filled"]\n')
    connectivity = loadtxt('outputs/connectivity.txt', dtype=int)
    amax = float(connectivity[:,-1].max())
    for i, j, a in connectivity:
        fh.write('{0} -> {1} [penwidth={2}, arrowsize={2}]\n'.format(
                 i, j, sqrt(a / amax)))
    fh.write('}')
