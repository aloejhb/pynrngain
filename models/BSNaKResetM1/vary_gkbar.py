import os
import sys
import copy
import numpy as np
import matplotlib.pyplot as plt
import plotvarygkbar
import labeldir
sys.path.append('../../')
from nrngain import jspar, transfer, spkstat
from runjob import submitjob as sbmj


def varygk_ficurve(gkbarli, curtvec, outdir, noise=0, tau=0):
    if not os.path.exists(outdir):
        raise OSError('No such output directory: {}'.format(outdir))
    for gkbar in gkbarli:
        gkdir = labeldir.gkbar_dir(gkbar)
        subdir = os.path.join(outdir, gkdir)
        if not os.path.exists(subdir):
            os.mkdir(subdir)
        ncellpar = {'gkbar': gkbar}
        cellpar = copy.copy(deflt_cellpar)
        cellpar.update(ncellpar)
        sbmj.run_ficurve(qname, curtvec, cellpar, spkthr, subdir, noise, tau)


def plot_ficurve(gkbarli, indir):
    for gkbar in gkbarli:
        gkdir = labeldir.gkbar_dir(gkbar)
        subdir = os.path.join(indir, gkdir)
        curtvec = np.load(os.path.join(subdir, 'curtvec.npy'))
        frtvec = np.load(os.path.join(subdir, 'frtvec.npy'))
        lab = labeldir.gkbar_lab(gkbar)
        plt.plot(curtvec, frtvec, 'o-', label=lab, ms=2., alpha=0.7)
        
    plt.xlabel('I (nA)')
    # plt.xlim((0, 0.2))
    plt.ylabel('Firing rate (Hz)')
    # plt.ylim((0, 80))
    plt.legend(loc=4, prop={'size': 7}, fancybox=True, framealpha=0.5)
    plt.minorticks_on()
    
    plt.savefig(os.path.join(indir, 'fi_curve.pdf'))
    plt.show()


def varygk_optstimpar(gkbarli, xzeroli, ttime, tau, frttarg, cvtarg, outdir_base):
    print 'Start to optimize stimpar ...'
    print 'gkbar_list: ' + str(gkbarli)
    print 'x0_list: ' + str(xzeroli)
    print 'tau: %.0f' % tau
    print 'frt: %.0f\tcv: %.1f' % (frttarg, cvtarg)

    optsubdir = labeldir.opt_subdir(tau, frttarg, cvtarg)
    outdir = os.path.join(outdir_base, optsubdir)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    for gkbar, x0 in zip(gkbarli, xzeroli):
        gkdir = labeldir.gkbar_dir(gkbar)
        subdir = os.path.join(outdir, gkdir)
        if not os.path.exists(subdir):
            os.mkdir(subdir)
        ncellpar = {'gkbar': gkbar}
        cellpar = copy.copy(deflt_cellpar)
        cellpar.update(ncellpar)
        sbmj.run_optstimpar(qname, subdir, cellpar, spkthr, x0, tau, ttime, frttarg, cvtarg)


def varygk_simulation(gkbarli, ttime, pardir_base, outdir_base):
    for gkbar in gkbarli:
        gkdir = labeldir.gkbar_dir(gkbar)
        pardir = os.path.join(pardir_base, gkdir)
        outdir = os.path.join(outdir_base, gkdir)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        sbmj.run_simulation(qname, ttime, outdir, pardir)


def varygk_sta(gkbarli, indir_base):
    for gkbar in gkbarli:
        gkdir = labeldir.gkbar_dir(gkbar)
        indir = os.path.join(indir_base, gkdir)
        if not os.path.exists(indir):
            raise OSError('No such directory: {}'.format(indir))
        sbmj.run_sta(qname, indir)


def varygk_spkstat(gkbarli, indir_base):
    for gkbar in gkbarli:
        gkdir = labeldir.gkbar_dir(gkbar)
        indir = os.path.join(indir_base, gkdir)
        if not os.path.exists(indir):
            raise OSError('No such directory: {}'.format(indir))
        spkstat.get_spkstat_from_file(indir)


def varygk_transfer(gkbarli, indir_base):
    for gkbar in gkbarli:
        gkdir = labeldir.gkbar_dir(gkbar)
        indir = os.path.join(indir_base, gkdir)
        transfer.run_transfer(indir)


if __name__ == '__main__':

    qname = 'fulla.q'
    gnabar = 0.005
    deflt_cellpar = {'pos_ais': 0.1,
                     'gnabar': gnabar,
                     'gkbar': 0.005,
                     'ap_thresh': -40}
    spkthr = -40

    figdir = '../../figures/BSNaKResetNew/'
    fidir = os.path.join(figdir, 'fi_curve')
    gksclli = [0, 1, 3]
    gkbarli = [gnabar * scl for scl in gksclli]
    curtvec = np.linspace(0, 0.2, 50)
    noise = 0
    tau = 30
    noisedir = 'std{:.3f}'.format(noise)
    noisefidir = os.path.join(fidir, noisedir)
    if not os.path.exists(noisefidir):
        os.mkdir(noisefidir)
    # varygk_ficurve(gkbarli, curtvec, noisefidir, noise, tau)
    # plot_ficurve(gkbarli, noisefidir)

    resdir = '../../results/BSNaKResetNew/'
    optdir = os.path.join(resdir, 'opt_stimpar')
    ttime = 20000.
    tau = 30
    cvtarg = 1.
    frttarg = 5.
    gksclli = [3]
    gkbarli = [gnabar * scl for scl in gksclli]
    xzeroli = [(0.05405543,  0.01104503)]
    # varygk_optstimpar(gkbarli, xzeroli, ttime, tau, frttarg, cvtarg, optdir)

    # simdir = '/scratch03/hubo/simulation/BSNaKResetNew/'
    simdir = '../../results/BSNaKResetNew/simulation'
    figdir = '../../figures/BSNaKResetNew'
    ttime = 2000000
    tauli = [5, 30]
    frttargli = [5, 10]
    for tau in tauli:
        for frttarg in frttargli:
            cvtarg = 1.
            gksclli = [0, 1, 3]
            # gksclli = [3]
            gkbarli = [gnabar * scl for scl in gksclli]
            optsubdir = labeldir.opt_subdir(tau, frttarg, cvtarg)
            optpath = labeldir.opt_path(tau, frttarg, cvtarg)
            pardir_base = os.path.join(optdir, optsubdir)
            simdir_base = os.path.join(simdir, optsubdir)
            print simdir_base
            # varygk_simulation(gkbarli, ttime, pardir_base, simdir_base)
            # varygk_sta(gkbarli, simdir_base)
            # varygk_spkstat(gkbarli, simdir_base)
            varygk_transfer(gkbarli, simdir_base)
            normalized = False
            if normalized:
                figname = 'gain_norm_'+optpath
            else:
                figname = 'gain_'+optpath
            figpath = os.path.join(figdir, 'gain', figname+'.pdf')
            print figpath
            plotvarygkbar.plot_gains(gkbarli, simdir_base, figpath, normalized=normalized, statlab=True)
    
