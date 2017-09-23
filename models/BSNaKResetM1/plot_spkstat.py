import os
import numpy as np
import matplotlib.pyplot as plt
import labeldir
import sys
sys.path.append('../..')
from nrngain import spkstatgraph as ssg


def plot_hists(indir, figpath, gkbarli, nbin=20):
    plt.figure()
    for gkbar in gkbarli:
        gkdir = labeldir.gkbar_dir(gkbar)
        subdir = os.path.join(indir, gkdir)
        spktimes = np.load(os.path.join(subdir, 'spktimes.npy'))
        gklab = labeldir.gkbar_lab(gkbar)
        ssg.plot_hist(spktimes, nbin, log=True, label=gklab)
    plt.xlabel('ISI (ms)')
    plt.ylabel('# ISI / total # ISI')
    plt.legend(loc=1, prop={'size': 14}, fancybox=True, framealpha=0.5)
    plt.savefig(figpath)


def plot_srcrs(indir, figpath, gkbarli, norder=10):
    plt.figure()
    for gkbar in gkbarli:
        gkdir = labeldir.gkbar_dir(gkbar)
        subdir = os.path.join(indir, gkdir)
        spktimes = np.load(os.path.join(subdir, 'spktimes.npy'))
        gklab = labeldir.gkbar_lab(gkbar)
        ssg.plot_srcr(spktimes, norder, label=gklab)
    plt.xlabel('Order')
    plt.ylabel('Spearman Rank Coefficient')
    plt.ylim((-0.025, 0.15))
    plt.legend(loc=1, prop={'size': 14}, fancybox=True, framealpha=0.5)
    plt.tight_layout()
    plt.savefig(figpath)


def targ_plot(tau, frttarg, cvtarg, indir, outdir, plotfunc,
              *pltargs, **pltkwargs):
    optsubdir = labeldir.opt_subdir(tau, frttarg, cvtarg)
    optpath = labeldir.opt_path(tau, frttarg, cvtarg)
    insubdir = os.path.join(indir, optsubdir)
    figpath = os.path.join(outdir, optpath+'.pdf')
    plotfunc(insubdir, figpath, *pltargs, **pltkwargs)


if __name__ == '__main__':
    gkbarli = [0, 5e-3, 15e-3]
    tauli = [5, 30]
    cvtarg = 1.
    frttargli = [5, 10]

    simdir = '../../results/BSNaKResetNew/simulation'
    ssgdir = '../../figures/BSNaKResetNew/spkstat_graph'

    histdir = os.path.join(ssgdir, 'hist')
    if not os.path.exists(histdir):
        os.makedirs(histdir)
    srcrdir = os.path.join(ssgdir, 'srcr')
    if not os.path.exists(srcrdir):
        os.makedirs(srcrdir)

    for tau in tauli:
        for frttarg in frttargli:
            # targ_plot(tau, frttarg, cvtarg, simdir, histdir, plot_hists, gkbarli)
            targ_plot(tau, frttarg, cvtarg, simdir, srcrdir, plot_srcrs, gkbarli)
    plt.show()
