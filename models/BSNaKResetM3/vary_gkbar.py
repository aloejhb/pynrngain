import os
import sys
import copy
import numpy as np
import matplotlib.pyplot as plt
import plotvarygkbar
import labeldir
from subprocess import call
sys.path.append('../../')
from nrngain import jspar, transfer, spkstat


def submit_to_cluster(jobname, script, args):
    args = [str(arg) for arg in args]
    command = ['qsub', '-N', jobname, 'submit.sh', script] + args
    call(command)


def run_ficurve(curtvec, cellpar, outdir, noise=0, tau=0):
    cpfile = os.path.join(outdir, 'cellpar.json')
    jspar.save(cpfile, cellpar)

    ctvfile = os.path.join(outdir, 'curtvec.npy')
    np.save(ctvfile, curtvec)

    args = [ctvfile, cpfile, spkthr, outdir, '--noise', noise, '--tau', tau]
    submit_to_cluster('ficurve', '../../run/run_ficurve.py', args)


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
        run_ficurve(curtvec, cellpar, subdir, noise, tau)


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


def run_optstimpar(outdir, cellpar, spkthr, x0, *optmargs):
    spkthrfile = os.path.join(outdir, 'spkthr.json')
    jspar.save(spkthrfile, spkthr)
    cpfile = os.path.join(outdir, 'cellpar.json')
    jspar.save(cpfile, cellpar)

    args = [outdir, cpfile, spkthr, x0[0], x0[1]]
    args.extend(optmargs)
    submit_to_cluster('optstm', '../../run/run_optstimpar.py', args)


def varygk_optstimpar(gkbarli, xzeroli, ttime, tau, frttarg, cvtarg, outdir_base):
    print 'Start to optimize stimpar ...'
    print 'gkbar_list: ' + str(gkbarli)
    print 'x0_list: ' +str(xzeroli)
    print 'tau: %.0f'% tau
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
        run_optstimpar(subdir, cellpar, spkthr, x0, tau, ttime, frttarg, cvtarg)


def run_simulation(ttime, outdir, pardir):
    spkthrfile = os.path.join(pardir, 'spkthr.json')
    cpfile = os.path.join(pardir, 'cellpar.json')
    spfile = os.path.join(pardir, 'stimpar.json')

    if not (os.path.exists(pardir) and os.path.isfile(cpfile) and os.path.isfile(spfile) and os.path.isfile(spkthrfile)):
        raise Exception('Please run run_optstimpar() before run_simulation()! pardir {}'.format(pardir))

    if not os.path.exists(outdir):
        raise OSError('No such directory: {}'.format(outdir))

    spkthr = jspar.load(spkthrfile)
    stimtyp = 'OU'
    args = [cpfile, spkthr, ttime, stimtyp, spfile, outdir]
    submit_to_cluster('sim', '../../run/run_simulation.py', args)


def varygk_simulation(gkbarli, ttime, pardir_base, outdir_base):
    for gkbar in gkbarli:
        gkdir = labeldir.gkbar_dir(gkbar)
        pardir = os.path.join(pardir_base, gkdir)
        outdir = os.path.join(outdir_base, gkdir)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        run_simulation(ttime, outdir, pardir)


def varygk_sta(gkbarli, indir_base):
    for gkbar in gkbarli:
        gkdir = labeldir.gkbar_dir(gkbar)
        indir = os.path.join(indir_base, gkdir)
        if not os.path.exists(indir):
            raise OSError('No such directory: {}'.format(indir))
        submit_to_cluster('sta', '../../run/run_sta.py', [indir])


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

    modeldir = 'BSNaKResetM3'
    gnabar = 0.001
    deflt_cellpar = {'pos_ais': 0.1,
                     'gnabar': gnabar,
                     'gkbar': 0.005,
                     'ap_thresh': -40}
    spkthr = -40

    figdir = os.path.join('../../figures', modeldir)
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
    plot_ficurve(gkbarli, noisefidir)

    resdir = os.path.join('../../results', modeldir)
    optdir = os.path.join(resdir, 'opt_stimpar')
    ttime = 100000.
    tau = 30
    cvtarg = 1.
    frttarg = 10
    gksclli = [3]
    gkbarli = [gnabar * scl for scl in gksclli]
    xzeroli = [(0.04059528,  0.01815964)]
    # varygk_optstimpar(gkbarli, xzeroli, ttime, tau, frttarg, cvtarg, optdir)

    simdir = os.path.join('../../results', modeldir, 'simulation')
    figdir = os.path.join('../../figures', modeldir)
    ttime = 2000000
    tauli = [5, 30]
    frttargli = [5, 10]
    for tau in tauli:
        for frttarg in frttargli:
            cvtarg = 1.
            gksclli = [0, 1, 3]
            gkbarli = [gnabar * scl for scl in gksclli]
            optsubdir = labeldir.opt_subdir(tau, frttarg, cvtarg)
            optpath = labeldir.opt_path(tau, frttarg, cvtarg)
            pardir_base = os.path.join(optdir, optsubdir)
            simdir_base = os.path.join(simdir, optsubdir)
            print simdir_base
            # varygk_simulation(gkbarli, ttime, pardir_base, simdir_base)
            # varygk_sta(gkbarli, simdir_base)
            # varygk_spkstat(gkbarli, simdir_base)
            # varygk_transfer(gkbarli, simdir_base)
            normalized = True
            if normalized:
                figname = 'gain_norm_'+optpath
            else:
                figname = 'gain_'+optpath
            figpath = os.path.join(figdir, 'gain', figname+'.pdf')
            # plotvarygkbar.plot_gains(gkbarli, simdir_base, figpath, normalized=normalized, statlab=True)
