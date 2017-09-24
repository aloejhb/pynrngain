import os
import numpy as np
import matplotlib.pyplot as plt
from .jspar import load as jsload
from .spkstat import get_spkstat_from_file
from .transfer import get_cutoff_freq


def get_statlab(indir):
    statfile = os.path.join(indir, 'spkstat.json')
    if not os.path.isfile(statfile):
        get_spkstat_from_file(indir)
    stat = jsload(statfile)
    stat_lab = '(frt:%.1f cv:%.2f lv:%.2f)' % (stat['frt'], stat['cv'], stat['lv'])
    return stat_lab


def plot_gain(indir, normalized=False, cutoff=False, **kwargs):
    transf = np.load(os.path.join(indir, 'transf.npy'))
    fvec = np.load(os.path.join(indir, 'fvec.npy'))
    gain = np.absolute(transf)
    if normalized:
        gain = gain / gain[1]
    plt.loglog(fvec, gain, **kwargs)
    if cutoff and not normalized:
        plot_cutoff(fvec, gain)


def plot_cutoff(indir):
    transf = np.load(os.path.join(indir, 'transf.npy'))
    fvec = np.load(os.path.join(indir, 'fvec.npy'))
    gain = np.absolute(transf)
    ind, cof, cog = get_cutoff_freq(fvec, gain, ind=True)
    plt.plot(cof, cog, 'o', color='k', alpha=0.5)
    plt.vlines(cof, 0, cog, color='black', linestyle='dashed', alpha=0.7)


def plot_transf(indir, **kwargs):
    transf = np.load(os.path.join(indir, 'transf.npy'))
    fvec = np.load(os.path.join(indir, 'fvec.npy'))
    gain = np.absolute(transf)
    phase = np.angle(transf)

    plt.subplot(121)
    plt.semilogx(fvec, gain, **kwargs)
    plt.subplot(122)
    plt.semilogx(fvec, phase, **kwargs)
