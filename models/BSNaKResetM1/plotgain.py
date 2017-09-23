import os
import numpy as np
import matplotlib.pyplot as plt
import labeldir
import sys
sys.path.append('../../')
from nrngain import transfer

def get_figname(norm, cutoff, phase):
    if phase:
        nameli = ['transf']
    else:
        nameli = ['gain']
    if norm:
        nameli.append('norm')
    if cutoff:
        nameli.append('cut')
    return '_'.join(nameli)


def plot_gain(indir, normalized=False, cutoff=False, **kwargs):
    transf = np.load(os.path.join(indir, 'transf.npy'))
    fvec = np.load(os.path.join(indir, 'fvec.npy'))
    gain = np.absolute(transf)
    if normalized:
        gain = gain / gain[1]
    plt.loglog(fvec, gain, **kwargs)
    if cutoff and not normalized:
        plot_cutoff(fvec, gain)


def plot_cutoff(fvec, gain):
    ind, cof, cog = transfer.get_cutoff_freq(fvec, gain, ind=True)
    plt.plot(cof, cog, 'o', color='k', alpha=0.5)
    plt.vlines(cof, 0, cog, color='black', linestyle='dashed', alpha=0.7)


def plot_gains(gkbarli, indir, figpath, normalized=False, cutoff=False):
    plt.figure()
    for gkbar in gkbarli:
        gkdir = labeldir.gkbar_dir(gkbar)
        subdir = os.path.join(indir, gkdir)
        transfdir = os.path.join(subdir, 'transfer')
        lab = labeldir.gkbar_lab(gkbar)
        plot_gain(transfdir, normalized, cutoff, label=lab)

    plt.xlabel('Frequency (Hz)')
    if normalized:
        plt.ylabel('Normalized gain')
        plt.ylim(bottom=0.01)
        if cutoff:
            plt.axhline(1/np.sqrt(2), color='black', linewidth=3, linestyle='dashed', alpha=0.4)
    else:
        plt.ylabel('Gain (Hz/nA)')
        plt.ylim(bottom=100)
    plt.legend(loc=1, prop={'size': 12}, fancybox=True, framealpha=0.5)
    plt.tight_layout()
    plt.savefig(figpath)


def plot_transf(indir, **kwargs):
    transf = np.load(os.path.join(indir, 'transf.npy'))
    fvec = np.load(os.path.join(indir, 'fvec.npy'))
    gain = np.absolute(transf)
    phase = np.angle(transf)

    plt.subplot(121)
    plt.semilogx(fvec, gain, **kwargs)
    plt.subplot(122)
    plt.semilogx(fvec, phase, **kwargs)


def plot_transfs(gkbarli, indir, figpath):
    plt.figure(figsize=(8, 4))
    for gkbar in gkbarli:
        gkdir = labeldir.gkbar_dir(gkbar)
        subdir = os.path.join(indir, gkdir)
        transfdir = os.path.join(subdir, 'transfer')
        lab = labeldir.gkbar_lab(gkbar)
        plot_transf(transfdir, label=lab)

    plt.subplot(121)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain (Hz/nA)')
    plt.legend(loc=1, prop={'size': 12}, fancybox=True, framealpha=0.5)
    plt.subplot(122)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Phase')
    plt.legend(loc=1, prop={'size': 12}, fancybox=True, framealpha=0.5)
    plt.tight_layout()
    plt.savefig(figpath)


if __name__ == '__main__':
    simdir = '../../results/BSNaKResetNew/simulation'
    figdir = '../../figures/BSNaKResetNew'
    cvtarg = 1.
    tauli = [5, 30]
    frttargli = [5, 10]
    # tauli = [30]
    # frttargli = [5]
    gkbarli = [0, 5e-3, 15e-3]
    phase = False
    norm = True
    cutoff = True
    for tau in tauli:
        for frttarg in frttargli:
            optsubdir = labeldir.opt_subdir(tau, frttarg, cvtarg)
            optpath = labeldir.opt_path(tau, frttarg, cvtarg)
            simdir_base = os.path.join(simdir, optsubdir)
            print simdir_base
            figname = get_figname(norm, cutoff, phase)+'_'+optpath
            figpath = os.path.join(figdir, 'gain', figname+'.pdf')
            if phase:
                plot_transfs(gkbarli, simdir_base, figpath)
            else:
                plot_gains(gkbarli, simdir_base, figpath, normalized=norm, cutoff=cutoff)
    plt.show()
