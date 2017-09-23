import os
import numpy as np
import matplotlib.pyplot as plt
import labeldir
import sys
sys.path.append('../..')
# from nrngain import transfer

def plot_bifdiag(curtvec, fpli, label=None, newfig=True, **kwargs):
    if newfig:
        plt.figure()
    for i, cur, fps in zip(range(len(curtvec)), curtvec, fpli):
        for j, fp in enumerate(fps):
            if i == 0 and j == 0:
                plt.plot(cur, fp, 'o', label=label, **kwargs)
            else:
                plt.plot(cur, fp, 'o', **kwargs)


def plot_bifurc(gkbar_list, indir, color_li):

    for i, gkbar in enumerate(gkbar_list):
        gkdir = labeldir.gkbar_dir(gkbar)
        subdir = os.path.join(indir, gkdir)
        curtvec = np.load(os.path.join(subdir, 'curtvec.npy'))
        fpli = np.load(os.path.join(subdir, 'fpli.npy'))
        lab = labeldir.gkbar_lab(gkbar)
        color = color_li[i]
        plot_bifdiag(curtvec, fpli, label=lab, newfig=False, color=color, ms=2., alpha=0.7)
        
    plt.xlabel('$I_{inpq}$ (nA)')
    # plt.xlim((0, 0.2))
    plt.ylabel('Membrane voltage at AIS (mV)')
    # plt.ylim((0, 80))
    plt.legend(loc=4, fancybox=True, framealpha=0.5)
    plt.minorticks_on()
    plt.tight_layout()
    plt.savefig('%s/bifurc.pdf' % indir)
    plt.show()

if __name__ == '__main__':
    figdir = '../../figures/BSNaKResetNew/'
    bfdir = os.path.join(figdir, 'bifurcation')

    gkbarli = [0, 5e-3, 15e-3]
    colorli = ['#1f77b4', '#ff7f0e', '#2ca02c']
    plot_bifurc(gkbarli, bfdir, colorli)
