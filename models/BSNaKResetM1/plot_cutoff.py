import os
import numpy as np
import matplotlib.pyplot as plt
import labeldir
import sys
sys.path.append('../..')
from nrngain import transfer


def targ_infunc(tau, frttarg, cvtarg, indir, func, *fargs, **fkwargs):
    optsubdir = labeldir.opt_subdir(tau, frttarg, cvtarg)
    insubdir = os.path.join(indir, optsubdir)
    return func(insubdir, *fargs, **fkwargs)


def varygk_cutoff(indir, gkbarli):
    cofreqli = []
    for gkbar in gkbarli:
        gkdir = labeldir.gkbar_dir(gkbar)
        subdir = os.path.join(indir, gkdir)
        transfdir = os.path.join(subdir, 'transfer')

        transf = np.load(os.path.join(transfdir, 'transf.npy'))
        fvec = np.load(os.path.join(transfdir, 'fvec.npy'))
        gain = np.absolute(transf)

        cofreq = transfer.get_cutoff_freq(fvec, gain)
        cofreqli.append(cofreq)
    return np.array(cofreqli)


def plot_varytau_cutoff(tauli, indir, outdir, frttarg, cvtarg, gkbarli, colorli, width=0.35):
    figname = 'cutoff_' + labeldir.targs_dir(frttarg, cvtarg)
    figpath = os.path.join(outdir, figname+'.pdf')
    ind = np.arange(len(gkbarli))
    gklabli = map(labeldir.gkbar_lab, gkbarli)
    print labeldir.targs_dir(frttarg, cvtarg)
    plt.figure()
    for i, tau in enumerate(tauli):
        cofreqli = targ_infunc(tau, frttarg, cvtarg, indir, varygk_cutoff, gkbarli)
        print 'tau', tau
        print cofreqli
        xshift = i*width
        color = colorli[i]
        plt.bar(ind + xshift, cofreqli, width, label=labeldir.tau_lab(tau), color=color)
    ax = plt.gca()
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(gklabli, fontsize=16)
    plt.ylabel('Cutoff frequency (Hz)')
    plt.legend(prop={'size': 15}, fancybox=True, framealpha=0.5)
    plt.ylim((0, 27))
    plt.tight_layout()
    plt.savefig(figpath)


if __name__ == '__main__':
    tauli = [5, 30]
    colorli = ['lightpink', 'royalblue']
    cvtarg = 1.0
    frttargli = [5, 10]
    simdir = '../../results/BSNaKResetNew/simulation'
    codir = '../../figures/BSNaKResetNew/cutoff'
    if not os.path.exists(codir):
        os.mkdir(codir)
    gkbarli = [0, 5e-3, 15e-3]
    for frttarg in frttargli:
        plot_varytau_cutoff(tauli, simdir, codir, frttarg, cvtarg, gkbarli, colorli)
    plt.show()
