import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import labeldir


# def find_thresh_ind(ivec, ithresh=0.001):
#     inds = np.where(np.diff(np.sign(ivec - ithresh)) > 0)[0]
#     if len(inds):
#         return inds[-1]
#     return None
def find_thresh_ind(ivec, ithresh=0.001):
    rivec = list(reversed(ivec))
    for j, cur in enumerate(rivec[1:]):
        if cur < ithresh and rivec[j-1] > ithresh:
            return len(rivec) - j
    return None


def get_slope(x, y, ind):
    return (y[ind+1] - y[ind]) / (x[ind+1] - x[ind])


def get_slope_list(fifos, xname, yname, iname, fir=10):
    xmat = fifos[xname][fir:]
    ymat = fifos[yname][fir:]
    imat = fifos[iname][fir:]

    slopeli = []
    for ivec, xvec, yvec in zip(imat, xmat, ymat):
        ind = find_thresh_ind(ivec)
        slope = get_slope(xvec, yvec, ind)
        slopeli.append(slope)
    return slopeli


def plot_varygk_slope(gkbarli, indir, xname, yname, iname='icap_ais', xlab='', figpath=None, binwidth=None):
    print 'x', xname, 'y', yname
    plt.figure()
    for gkbar in gkbarli:
        gklab = labeldir.gkbar_lab(gkbar)
        gkdir = labeldir.gkbar_dir(gkbar)
        subdir = os.path.join(indir, gkdir)
        with open(os.path.join(subdir, 'fifos.p')) as f:
            fifos = pickle.load(f)
        slopeli = get_slope_list(fifos, xname, yname, iname)
        print np.mean(slopeli)

        if binwidth:
            bins = np.arange(min(slopeli), max(slopeli) + binwidth, binwidth)
            plt.hist(slopeli, label=gklab, alpha=0.7, bins=bins)
        else:
            plt.hist(slopeli, label=gklab, alpha=0.7)

    plt.xlabel(xlab)
    plt.ylabel('# spikes')
    plt.legend(prop={'size': 12}, fancybox=True, framealpha=0.5)
    plt.tight_layout()
    if figpath:
        plt.savefig(figpath)


def get_vthr_list(fifos, vname, iname, fir=10):
    vmat = fifos[vname][fir:]
    imat = fifos[iname][fir:]

    vthrli = []
    for ivec, vvec in zip(imat, vmat):
        ind = find_thresh_ind(ivec)
        vthrli.append(vvec[ind])
    return vthrli


def plot_varygk_vthr(gkbarli, indir, vname='v_ais', iname='icap_ais', figpath=None, binwidth=None):
    print vname
    plt.figure()
    for gkbar in gkbarli:
        gklab = labeldir.gkbar_lab(gkbar)
        gkdir = labeldir.gkbar_dir(gkbar)
        subdir = os.path.join(indir, gkdir)
        with open(os.path.join(subdir, 'fifos.p')) as f:
            fifos = pickle.load(f)
        vthrli = get_vthr_list(fifos, vname, iname)
        print np.mean(vthrli)

        if binwidth:
            bins = np.arange(min(vthrli), max(vthrli) + binwidth, binwidth)
            plt.hist(vthrli, label=gklab, alpha=0.7, bins=bins)
        else:
            plt.hist(vthrli, label=gklab, alpha=0.7)

    plt.xlabel('Voltage at threshold (mV)')
    plt.ylabel('# spikes')
    plt.legend(prop={'size': 12}, fancybox=True, framealpha=0.5)

    plt.tight_layout()
    if figpath:
        plt.savefig(figpath)


def get_figpath(outdir, pref, appd):
    figname = '_'.join(('thresh', pref, appd))
    figpath = os.path.join(outdir, figname+'.pdf')
    return figpath


if __name__ == '__main__':
    ppdir = '../../figures/BSNaKResetNew/phase_plane'
    thrdir = '../../figures/BSNaKResetNew/threshold'
    cvtarg = 1.
    tauli = [5]#, 30]
    frttargli = [5]#, 10]
    tauli = [5, 30]
    bwli1 = [5, 0.8]
    bwli2 = [0.0004, 0.00005]
    bwli3 = [0.0025, 0.002]
    bwli4 = [0.004, 0.0025]

    frttargli = [5, 10]
    gkbarli = [0, 5e-3, 15e-3]
    for i, tau in enumerate(tauli):
        for frttarg in frttargli:
            optsubdir = labeldir.opt_subdir(tau, frttarg, cvtarg)
            optsublab = labeldir.opt_path(tau, frttarg, cvtarg)
            print optsublab
            ppsubdir = os.path.join(ppdir, optsubdir)

            figpath = None
            figpath = get_figpath(thrdir, 'vthr', optsublab)
            binwidth = bwli1[i]
            plot_varygk_vthr(gkbarli, ppsubdir, 'v_ais', 'icap_ais', figpath=figpath, binwidth=binwidth)

            figpath = get_figpath(thrdir, 'iv', optsublab)
            binwidth = bwli2[i]
            plot_varygk_slope(gkbarli, ppsubdir, 'v_ais', 'icap_ais', xlab='$dI_c/dV$ (mAcm$^{-2}$/mV)', figpath=figpath, binwidth=binwidth)

            
            figpath = get_figpath(thrdir, 'mv', optsublab)
            binwidth = bwli3[i]
            plot_varygk_slope(gkbarli, ppsubdir, 'v_ais', 'nav_m', xlab='dm/dV (/mV)', figpath=figpath, binwidth=binwidth)
            
            figpath = get_figpath(thrdir, 'mt', optsublab)
            binwidth = bwli4[i]
            plot_varygk_slope(gkbarli, ppsubdir, 'time', 'nav_m', xlab='dm/dt (/ms)', figpath=figpath, binwidth=binwidth)
    plt.show()
