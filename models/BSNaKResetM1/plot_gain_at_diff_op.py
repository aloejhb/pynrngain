import os
import numpy as np
import matplotlib.pyplot as plt
import labeldir
import sys
import plotgain
sys.path.append('../../')
from nrngain import transfer

simdir = '../../results/BSNaKResetNew/simulation'
figdir = '../../figures/BSNaKResetNew'
tau = 30
gkbar = 15e-3
phase = False
norm = True
cutoff = False
plt.figure()
frtli = [5, 5, 10]
cvli = [1, 1.3, 1]
colorli = ['#fb3b3b', '#f4a259', '#58a658']
for frttarg, cvtarg, color in zip(frtli, cvli, colorli):
    optsubdir = labeldir.opt_subdir(tau, frttarg, cvtarg)
    optpath = labeldir.opt_path(tau, frttarg, cvtarg)
    simdir_base = os.path.join(simdir, optsubdir)
    print simdir_base
    figname = plotgain.get_figname(norm, cutoff, phase) + '_' + 'diffop'
    figpath = os.path.join(figdir, 'gain', figname+'.pdf')

    indir = simdir_base
    gkdir = labeldir.gkbar_dir(gkbar)
    subdir = os.path.join(indir, gkdir)
    transfdir = os.path.join(subdir, 'transfer')
    lab = labeldir.targs_lab(frttarg, cvtarg)
    plotgain.plot_gain(transfdir, norm, cutoff, label=lab, color=color)

    plt.xlabel('Frequency (Hz)')
    if norm:
        plt.ylabel('Normalized gain')
        plt.ylim(bottom=0.01)
        if cutoff:
            plt.axhline(1/np.sqrt(2), color='grey', linewidth=2, linestyle='dashed', alpha=0.5)
    else:
        plt.ylabel('Gain (Hz/nA)')
        plt.ylim(bottom=0)
    plt.legend(loc=1, prop={'size': 12}, fancybox=True, framealpha=0.5)
    plt.tight_layout()
    plt.savefig(figpath)

plt.show()
