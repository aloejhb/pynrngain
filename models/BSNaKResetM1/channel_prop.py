import os
import numpy as np
import matplotlib.pyplot as plt

import sys
from math import exp
from neuron import h
sys.path.append('../../')
import nrngain.channel as chnl


def get_navvecs(vvec):
    soma = h.Section(name='soma')

    nav = h.Nav_point(soma(0.5))
    nav.gnabar = 1.
    navvecs = chnl.channel_varvec(nav, ('minf', 'mtau'), vvec)
    return navvecs


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



if __name__ == '__main__':
    h.celsius = 25.

    soma = h.Section(name='soma')
    vvec = np.linspace(-100, 50, 50)

    nav = h.Nav_point(soma(0.5))
    nav.gnabar = 1.
    navvecs = chnl.channel_varvec(nav, ('minf', 'mtau'), vvec)

    kv = h.Kv7_point(soma(0.5))
    kv.gbar = 1.
    kvvecs = chnl.channel_varvec(kv, ('ninf', 'ntau'), vvec)
    import pdb; pdb.set_trace()


    figdir = '../../figures/BSNaKResetNew/channel'
    figname = 'nav_kv'
    plt.figure(figsize=(8,4))
    plt.subplot(121)
    plt.plot(vvec, navvecs['minf'], label='Nav $m_{\\inf}$')
    plt.plot(vvec, kvvecs['ninf'], label='Kv $n_{\\inf}$')
    plt.xlabel('Voltage (mV)')
    plt.ylabel('')
    plt.legend()
    plt.subplot(122)
    plt.plot(vvec, navvecs['mtau'], label='Nav $\\tau_m$')
    plt.plot(vvec, kvvecs['ntau'], label='Kv $\\tau_n$')
    plt.xlabel('Voltage (mV)')
    plt.ylabel('Time constant (ms)')
    plt.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(figdir, figname+'.pdf'))
    plt.show()
