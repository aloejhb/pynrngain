import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import copy
import labeldir
from submit import submit_to_cluster
sys.path.append('../..')
from nrngain import jspar


def targ_lab(statname, targ, dirlab=False):
    if statname == 'frt':
        tlab = '%.1f' % targ
    else:
        tlab = '%.2f' % targ

    if dirlab:
        return '-'.join((statname, tlab))
    return ' '.join((statname, tlab))


def run_contour(fxvec, bracket, xname, tau, statname, targ, ttime, cpfile, spkthr, outdir, jobname='contour'):
    fxvfile = os.path.join(outdir, 'fxvec.npy')
    np.save(fxvfile, fxvec)
    args = [outdir, cpfile, spkthr, fxvfile, bracket[0], bracket[1], xname, tau, statname, targ, ttime]
    submit_to_cluster(jobname, '../../run/run_contour.py', args)


def run_contours(outdir_base, cellpar, spkthr, bracket, statname, targ_list, fxvec, xname, tau, ttime, fvsplit=None):
    spkthrfile = os.path.join(outdir_base, 'spkthr.json')
    jspar.save(spkthrfile, spkthr)
    cpfile = os.path.join(outdir_base, 'cellpar.json')
    jspar.save(cpfile, cellpar)

    for targ in targ_list:
        outdir = os.path.join(outdir_base, targ_lab(statname, targ, dirlab=True))
        if not os.path.exists(outdir):
            os.mkdir(outdir)
            
        if fvsplit:
            spfxvec = np.split(fxvec, fvsplit)
            for i, fxv in enumerate(spfxvec):
                subdir = os.path.join(outdir, '%.2d' % i)
                if not os.path.exists(subdir):
                    os.mkdir(subdir)
                run_contour(fxv, bracket, xname, tau, statname, targ, ttime, cpfile, spkthr, subdir)
        else:
            jobname = 'ctg{:.0f}t{:.0f}'.format(cellpar['gkbar']*1e3, targ)
            run_contour(fxvec, bracket, xname, tau, statname, targ, ttime, cpfile, spkthr, outdir, jobname)


def varygk_contours(gkbarli, bracketli, outdir, *args, **kwargs):
    for i, gkbar in enumerate(gkbarli):
        gkdir = labeldir.gkbar_dir(gkbar)
        subdir = os.path.join(outdir, gkdir)
        if not os.path.exists(subdir):
            os.mkdir(subdir)
        ncellpar = {'gkbar': gkbar}
        cellpar = copy.copy(deflt_cellpar)
        cellpar.update(ncellpar)
        bracket = bracketli[i]
        run_contours(subdir, cellpar, spkthr, bracket, *args, **kwargs)


def plot_contour(indir, newfig=True, **kwargs):
    if newfig:
        plt.figure()

    mnvec = np.array(())
    sdvec = np.array(())

    for wd in sorted(os.listdir(indir)):
        wpath = os.path.join(indir, wd)
        ctpar = jspar.load(os.path.join(wpath, 'ctpar.json'))
        xname = ctpar['xname']
        fxvec = np.load(os.path.join(wpath, 'fxvec.npy'))
        xvec = np.load(os.path.join(wpath, 'xvec.npy'))
        if xname == 'std':
            mnvec = np.concatenate((mnvec, fxvec))
            sdvec = np.concatenate((sdvec, xvec))
        elif xname == 'mean':
            mnvec = np.concatenate((mnvec, xvec))
            sdvec = np.concatenate((sdvec, fxvec))
        else:
            raise ValueError('xname not belong to std or mean')

    # Remove nan in the arrays
    nanind = np.logical_or(np.isnan(mnvec), np.isnan(sdvec))
    mnvec = mnvec[~nanind]
    sdvec = sdvec[~nanind]
    # Sort arrays
    mnvec, sdvec = zip(*sorted(zip(mnvec, sdvec)))
    plt.plot(mnvec, sdvec, **kwargs)

    if newfig:
        # plt.ylim((0, 0.25))
        plt.legend()
        plt.savefig(os.path.join(indir, 'contour.pdf'))


def plot_contours(statname_list, targli_list, marker_list, indir_base, figname):
    plt.figure()
    
    for statname, targli, marker in zip(statname_list, targli_list, marker_list):
        for targ in targli:
            tlab = targ_lab(statname, targ)
            tdir = targ_lab(statname, targ, dirlab=True)
            indir = os.path.join(indir_base, tdir)
            plot_contour(indir, False, marker=marker, label=tlab)
        
    plt.ylim((0, 0.16))
    plt.xlim((0, 0.10))
    plt.xlabel('mean of OU input (nA)')
    plt.ylabel('std of OU input (nA)')
    plt.legend()
    plt.savefig(os.path.join(indir_base, figname+'.pdf'))


def plot_regime(thr, mndrvyli):
    plt.axvspan(0, thr, facecolor='lightgrey', alpha=0.4)
    poly = patches.Polygon([(thr, 0), (0.1, 0), (0.1, mndrvyli[1]), (thr, mndrvyli[0])], color='pink', alpha=0.4)
    ax = plt.gca()
    ax.add_artist(poly)
    

def plot_operpoint(gkbar, spdir, frtli, colorli, cv=1, rad=0.005):
    gkdir = labeldir.gkbar_dir(gkbar)
    for i, frt in enumerate(frtli):
        targsdir = labeldir.targs_dir(frt, cv)
        indir = os.path.join(spdir, targsdir, gkdir)
        stimpar = jspar.load(os.path.join(indir, 'stimpar.json'))
        yrad = 2 * rad
        color = colorli[i]
        ell = patches.Ellipse((stimpar['mean'], stimpar['std']), rad, yrad, color=color, alpha=0.5)
        ax = plt.gca()
        ax.add_artist(ell)

if __name__ == '__main__':
    gnabar = 0.005
    deflt_cellpar = {'pos_ais': 0.1,
                     'gnabar': gnabar,
                     'gkbar': 0.005,
                     'ap_thresh': -40}
    spkthr = -40

    figmoddir = '../../figures/BSNaKResetNew'

    ctrdir = os.path.join(figmoddir, 'contour')

    ttime = 2000
    # ttime = 50000

    fxvec = np.linspace(0.001, 0.04, 10)
    xname = 'mean'
    tau = 30
    # tau = 5

    taudir = labeldir.tau_dir(tau)
    subctrdir = os.path.join(ctrdir, taudir)
    if not os.path.exists(subctrdir):
        os.makedirs(subctrdir)

    # statname = 'frt'
    # # targ_list = [5., 10., 20.]
    # targ_list = [20.]


    # gkbarli = [5e-3]#, 5e-3, 15e-3]
    # bracketli = [(0.045, 0.06)]#, (0.04, 0.06), (0.065, 0.08)]
    # varygk_contours(gkbarli, bracketli, subctrdir, statname, targ_list, fxvec, xname, tau, ttime)
    statname_list = ['frt', 'cv', 'lv']
    targli_list = [[5, 10, 20], [0.5, 1, 1.5], [0.8, 1.0, 1.2]]
    marker_list = ['o', '+', '>']

    gkbar_list = [0, 5e-3, 15e-3]
    thrli = [0.0215, 0.0305, 0.058]
    mndrvylili = [(0.0170, 0.0690), (0.0230, 0.0680), (0.0287, 0.06)]
    for i, gkbar in enumerate(gkbar_list):
        gkdir = labeldir.gkbar_dir(gkbar)
        outdir_base = os.path.join(subctrdir, gkdir)

        stnnum = 2
        figname = 'contours_%s' % statname_list[stnnum - 1]
        plot_contours(statname_list[:stnnum], targli_list[:stnnum], marker_list, outdir_base, figname)
        if stnnum == 2:
            plot_regime(thrli[i], mndrvylili[i])
            rfigname = figname + '_regime'
            plt.savefig(os.path.join(outdir_base, rfigname+'.pdf'))
            optdir = '../../results/BSNaKResetNew/opt_stimpar/'
            spdir = os.path.join(optdir, taudir)
            frtli = [5, 10]
            opcolorli = ['r', 'forestgreen']
            plot_operpoint(gkbar, spdir, frtli, opcolorli)
            ofigname = figname + '_op'
            plt.savefig(os.path.join(outdir_base, ofigname+'.pdf'))
            
    plt.show()
