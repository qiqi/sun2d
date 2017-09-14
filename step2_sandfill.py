from numpy import *

from sun2d_utils import *

i, j = loadtxt('inputs/ij.txt', dtype=int).T
flags = loadhex('outputs/parts.txt')

savetxt('outputs/level_00.txt', flags[:,newaxis], fmt='%016X')
for i_level in range(1, 33):
    new_flags = flags.copy()
    bitwise_or.at(new_flags, i, flags[j])
    bitwise_or.at(new_flags, j, flags[i])
    flags = new_flags
    fname = 'outputs/level_{:02d}.txt'.format(i_level)
    savetxt(fname, flags[:,newaxis], fmt='%016X')
