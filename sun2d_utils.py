from numpy import *

def loadhex(fname):
    text = open(fname).read().replace('\n', '')
    return frombuffer(bytearray.fromhex(text), uint64).byteswap()
