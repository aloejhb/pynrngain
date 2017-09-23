import numpy as np
import matplotlib.pyplot as plt
from neuron import h

def channel_var(chan, varnames, v):
    chan.rates(v)
    vals = {varname: getattr(chan, varname) for varname in varnames}
    return vals


def channel_varvec(chan, varnames, vvec):
    vecs = {varname: [] for varname in varnames}
    for v in vvec:
        vals = channel_var(chan, varnames, v)
        for varname in varnames:
            vecs[varname].append(vals[varname])
    return vecs

if __name__ == '__main__':
    pass


