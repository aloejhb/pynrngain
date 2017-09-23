import os
import numpy as np
import matplotlib.pyplot as plt
import sys
import labeldir
sys.path.append('../../')
from nrngain import jspar, spkstat


def plot_gains(tauli, indir, gkbar, frttarg, cvtarg, figpath, normalized=False, statlab=False):

    plt.figure(figsize=(8, 4))

    gkdir = labeldir.gkbar_dir(gkbar)

    firgain = 0
    for i, tau in enumerate(tauli):
        optsubdir = labeldir.opt_subdir(tau, frttarg, cvtarg)
        subdir = os.path.join(indir, optsubdir, gkdir)
        transfdir = os.path.join(subdir, 'transfer')

        transf = np.load(os.path.join(transfdir, 'transf.npy'))
        fvec = np.load(os.path.join(transfdir, 'fvec.npy'))
        gain = np.absolute(transf)
        phase = np.angle(transf)

        if normalized:
            gain = gain / gain[1]

        lab = labeldir.tau_lab(tau)
        if statlab:
            statfile = os.path.join(subdir, 'stat.json')
            if not os.path.isfile(statfile):
                spkstat.get_stat_from_file(subdir)
            stat = jspar.load(statfile)
            stat_lab = '(frt:%.1f cv:%.2f lv:%.2f)' % (stat['frt'], stat['cv'], stat['lv'])
            lab = lab + ' ' + stat_lab

        plt.subplot(121)
        plt.semilogx(fvec, gain, label=lab)
        
        plt.subplot(122)
        plt.semilogx(fvec, phase, label=lab)

    plt.subplot(121)
    plt.xlabel('$f$ (Hz)')
    if normalized:
        plt.ylabel('Gain')
    else:
        plt.ylabel('Gain (Hz/nA)')
    # plt.ylim(5e5, 2e6)
    plt.legend(loc=1, prop={'size': 8}, fancybox=True, framealpha=0.5)

    plt.subplot(122)
    plt.xlabel('$f$ (Hz)')
    plt.ylabel('Phase')
    # plt.legend(prop={'size':8}, loc=4)
    plt.legend(loc=1, prop={'size': 8}, fancybox=True, framealpha=0.5)
    plt.tight_layout()

    if figpath:
        plt.savefig(figpath)


if __name__ == '__main__':
    # gkbarli = [0, 5e-3, 15e-3]
    indir = '../../results/BSNaKResetNew/simulation/'
    figdir = '../../figures/BSNaKResetNew/gain'
    tauli = [5, 30]
    frttarg = 5.0
    cvtarg = 1.0
    gkbar = 15e-3
    gkdir = labeldir.gkbar_dir(gkbar)
    targsdir = labeldir.targs_dir(frttarg, cvtarg)
    figpath = os.path.join(figdir, '_'.join(['gain', gkdir, targsdir])+'.pdf')
    plot_gains(tauli, indir, gkbar, frttarg, cvtarg, figpath, normalized=True)
    plt.show()
