import os
import numpy as np
import matplotlib.pyplot as plt

import sys
from math import exp
from neuron import h
sys.path.append('../../')
import nrngain.channel as chnl

h.celsius = 25.

soma = h.Section(name='soma')
vvec = np.linspace(-100, 50, 50)

nav = h.Nav_point(soma(0.5))
nav.gnabar = 1.
navvecs = chnl.channel_varvec(nav, ('minf', 'mtau'), vvec)

navhh = h.NavHHPoint(soma(0.5))
navhh.gnabar = 1.
navhhvecs = chnl.channel_varvec(navhh, ('minf', 'mtau'), vvec)
vvec_long = np.linspace(-400, 200, 50)
navhhvecs_long = chnl.channel_varvec(navhh, ('minf', 'mtau'), vvec_long)

figdir = '../../figures/BSNaKResetM3/channel'
def plot_m(vvec, chnlvecs, figname):
    plt.figure(figsize=(8,4))
    plt.subplot(121)
    plt.plot(vvec, chnlvecs['minf'])
    plt.xlabel('Voltage (mV)')
    plt.ylabel('minf')
    plt.subplot(122)
    plt.plot(vvec, chnlvecs['mtau'])
    plt.xlabel('Voltage (mV)')
    plt.ylabel('mtau (ms)')
    plt.tight_layout()
    plt.savefig(os.path.join(figdir, figname+'.pdf'))

# plot_m(vvec, navvecs, 'channel_Brette')
# plot_m(vvec, navhhvecs, 'channel_Schmidt')
# plot_m(vvec_long, navhhvecs_long, 'channel_Schmidt_longv')

def hrates(v):
    p6 = 9.896e-4

    p7 = 25.16
    p8 = 5.007
    p9 = 8.052
    p10 = 16.78
    
    alpha = p6 * exp(v/p7)
    beta = p8 / (exp(-(v+p9)/p10) - 1)
    htau = 1 / (alpha + beta)
    hinf = alpha * htau
    return htau

def rates(v):
    p1 = 136.4
    p2 = 113.1
    p3 = 19.35
    p4 = 0.3593
    p5 = 25.31

    alpha = - p1 * (v - p2) / (exp(-(v-p2)/p3) - 1)
    beta = p4 * exp(-v/p5)
    mtau = 1 / (alpha + beta)
    minf = alpha * mtau
    return minf, mtau


vvec = np.linspace(-100, 50, 50)
# print rates(-100), rates(-50), rates(0)
vrates = np.vectorize(rates)
# vhrates = np.vectorize(hrates)
minf, mtau = vrates(vvec)
plt.figure()
plt.plot(vvec, minf)
plt.xlabel('Voltage (mV)')
plt.ylabel('minf')
plt.figure()
plt.plot(vvec, mtau)
plt.xlabel('Voltage (mV)')
plt.ylabel('mtau(ms)')

# plt.plot(vvec, vhrates(vvec))


plt.show()
