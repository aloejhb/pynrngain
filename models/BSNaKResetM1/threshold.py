import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import labeldir


# def find_thresh_ind(ivec, ithresh=0.002):
#     for j, cur in enumerate(ivec):
#         if cur > ithresh and ivec[j-1] < ithresh:
#             return j
#     return None
def find_thresh_ind(ivec, ithresh=0.001):
    rivec = list(reversed(ivec))
    for j, cur in enumerate(rivec[1:]):
        if cur < ithresh and rivec[j-1] > ithresh:
            return len(rivec) - j
    return None


def iv_slope(vvec, ivec, ind):
    slope = (ivec[ind+1] - ivec[ind]) / (vvec[ind+1] - vvec[ind])
    return slope


def get_ivslope_list(fifos, fir=50):
    vmat = fifos['v_ais'][fir:]
    imat = fifos['icap_ais'][fir:]
    mmat = fifos['nav_m'][fir:]

    vthrli = []
    ivslopeli = []
    mvslopeli = []
    indli = []
    for j, ivec in enumerate(imat):
        ind = find_thresh_ind(ivec)
        indli.append(ind)
        vvec = vmat[j]
        ivslope = iv_slope(vvec, ivec, ind)
        ivslopeli.append(ivslope)
        mvec = mmat[j]
        mvslope = iv_slope(vvec, mvec, ind)
        mvslopeli.append(mvslope)
        vthrli.append(vvec[ind])
    return vthrli, ivslopeli, mvslopeli, indli


def get_slope(x, y, ind):
    return (y[ind+1] - y[ind]) / (x[ind+1] - x[ind])


def get_slope_list(fifos, xname, yname, iname, fir=50):
    xmat = fifos[xname][fir:]
    ymat = fifos[yname][fir:]
    imat = fifos[iname][fir:]

    slopeli = []
    for ivec, xvec, yvec in zip(imat, xmat, ymat):
        ind = find_thresh_ind(ivec)
        slope = get_slope(xvec, yvec, ind)
        slopeli.append(slope)
    return slopeli
    


def varygk_ivslope(gkbar, ppsubdir):
    gkdir = labeldir.gkbar_dir(gkbar)
    indir = os.path.join(ppsubdir, gkdir)
    with open(os.path.join(indir, 'fifos.p')) as f:
        fifos = pickle.load(f)
    return get_ivslope_list(fifos)


def plot_thresh_hists(gkbarli, figpath):
    plt.figure(figsize=(23, 5))
    for gkbar in gkbarli:
        gklab = labeldir.gkbar_lab(gkbar)
        vthrli, ivslopeli, mvslopeli, indli = varygk_ivslope(gkbar, ppsubdir)

        gkdir = labeldir.gkbar_dir(gkbar)
        indir = os.path.join(ppsubdir, gkdir)
        with open(os.path.join(indir, 'fifos.p')) as f:
            fifos = pickle.load(f)
        mtslopeli = get_slope_list(fifos, 'time', 'nav_m', 'icap_ais')


        print gkbar
        print 'nspk', len(vthrli)
        print 'v', np.mean(vthrli)
        print 'didv', np.mean(ivslopeli)
        print 'dmdv', np.mean(mvslopeli)
        print 'dmdt', np.mean(mtslopeli)
        print 't2spk', 40 - np.mean(indli)*0.025


        plt.subplot(141)
        plt.hist(vthrli, alpha=0.7, label=gklab)
        plt.subplot(142)
        plt.hist(ivslopeli, alpha=0.7, label=gklab)
        plt.subplot(143)
        plt.hist(mvslopeli, alpha=0.7, label=gklab)
        plt.subplot(144)
        plt.hist(mtslopeli, alpha=0.7, label=gklab)

    plt.subplot(141)
    plt.xlabel('Voltage at threshold (mV)')
    plt.ylabel('# spikes')
    plt.legend(prop={'size': 12}, fancybox=True, framealpha=0.5)

    plt.subplot(142)
    plt.xlabel('dI/dV (nA/mV)')
    plt.ylabel('# spikes')
    plt.legend(prop={'size': 12}, fancybox=True, framealpha=0.5)

    plt.subplot(143)
    plt.xlabel('dm/dV (/mV)')
    plt.ylabel('# spikes')
    plt.legend(prop={'size': 12}, fancybox=True, framealpha=0.5)

    plt.subplot(144)
    plt.xlabel('dm/dt (/ms)')
    plt.ylabel('# spikes')
    plt.legend(prop={'size': 12}, fancybox=True, framealpha=0.5)

    plt.tight_layout()
    plt.savefig(figpath)


if __name__ == '__main__':
    ppdir = '../../figures/BSNaKResetNew/phase_plane'
    thrdir = '../../figures/BSNaKResetNew/threshold'
    cvtarg = 1.
    tauli = [5, 30]
    frttargli = [5, 10]
    gkbarli = [0, 5e-3, 15e-3]
    for tau in tauli:
        for frttarg in frttargli:
            optsubdir = labeldir.opt_subdir(tau, frttarg, cvtarg)
            print optsubdir
            ppsubdir = os.path.join(ppdir, optsubdir)
            figname = 'thresh_' + labeldir.opt_path(tau, frttarg, cvtarg)
            print figname
            figpath = os.path.join(thrdir, figname+'.pdf')
            plot_thresh_hists(gkbarli, figpath)
    plt.show()



