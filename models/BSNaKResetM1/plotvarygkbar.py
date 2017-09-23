import os
import numpy as np
import matplotlib.pyplot as plt
import sys
import labeldir
sys.path.append('../../')
from nrngain import jspar, spkstat


def plot_gains(gkbarli, indir, figpath, normalized=False, statlab=False):

    plt.figure(figsize=(8, 4))

    for gkbar in gkbarli:
        gkdir = labeldir.gkbar_dir(gkbar)
        subdir = os.path.join(indir, gkdir)
        transfdir = os.path.join(subdir, 'transfer')

        transf = np.load(os.path.join(transfdir, 'transf.npy'))
        fvec = np.load(os.path.join(transfdir, 'fvec.npy'))
        gain = np.absolute(transf)
        phase = np.angle(transf)
        phase = np.negative(phase) ## this is used before changing phase to negative in transfer.py

        lab = labeldir.gkbar_lab(gkbar)
        if statlab:
            statfile = os.path.join(subdir, 'spkstat.json')
            if not os.path.isfile(statfile):
                spkstat.get_spkstat_from_file(subdir)
            stat = jspar.load(statfile)
            stat_lab = '(frt:%.1f cv:%.2f lv:%.2f)' % (stat['frt'], stat['cv'], stat['lv'])
            lab = lab + ' ' + stat_lab

        if normalized:
            gain = gain / gain[1]

        plt.subplot(121)
        plt.semilogx(fvec, gain, label=lab)
        
        plt.subplot(122)
        plt.semilogx(fvec, phase, label=lab)

    plt.subplot(121)
    plt.xlabel('Frequency (Hz)')
    if normalized:
        plt.ylabel('Gain')
    else:
        plt.ylabel('Gain (Hz/nA)')
    # plt.ylim(5e5, 2e6)
    plt.legend(loc=1, prop={'size': 8}, fancybox=True, framealpha=0.5)

    plt.subplot(122)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Phase')
    # plt.legend(prop={'size':8}, loc=4)
    plt.legend(loc=1, prop={'size': 8}, fancybox=True, framealpha=0.5)
    plt.tight_layout()

    if figpath:
        plt.savefig(figpath)


if __name__ == '__main__':
    gkbarli = [0, 5e-3, 15e-3]
    indir = '../../results/BSNaKResetNew/simulation/tau30/frt10_cv1-0'
    figpath = None
    plot_gains(gkbarli, indir, figpath)
    plt.show()
