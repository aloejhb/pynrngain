import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import labeldir
import threshold
import run
import sys
sys.path.append('../..')
from nrngain import jspar
import nrngain.phaseplane as pp


def get_ffind(t, ffstart, dt):
    return int((t-ffstart) / dt)


def get_var_at_thresh(fifos, thrindli, varname):
    return [fifos[varname][i][ind] for i, ind in enumerate(thrindli)]

def plot_align(fifos, yname, trng, fifo_trange, dt, **kwargs):
    tmat = np.tile(np.arange(fifo_trange[0], fifo_trange[1], dt), (len(fifos[yname]), 1))
    rng = map(lambda x: get_ffind(x, fifo_trange[0], dt), trng)
    pp.plot_multi_traj(tmat, fifos[yname], fir=15, num=20, rng=rng, **kwargs)


def plot_traj(fifos, xname, yname, trng, fifo_trange, dt, label='', **kwargs):
    rng = map(lambda x: get_ffind(x, fifo_trange[0], dt), trng)
    pp.plot_multi_traj(fifos[xname], fifos[yname], fir=15, num=20, rng=rng, label=label, **kwargs)


def plot_thresh(fifos, xname, yname, iname='icap_ais', ithresh=0.001, **kwargs):
    thrindli = map(lambda x: threshold.find_thresh_ind(x, ithresh), fifos[iname])
    thrlis = {}
    thrlis[xname] = get_var_at_thresh(fifos, thrindli, xname)
    thrlis[yname] = get_var_at_thresh(fifos, thrindli, yname)
    plt.plot(thrlis[xname], thrlis[yname], 'o', **kwargs)


def plot_thresh2(xvec, yvec, ivec, ithresh=0.001, **kwargs):
    thrindli = map(lambda x: threshold.find_thresh_ind(x, ithresh), ivec)
    xli = [xvec[i][ind] for i, ind in enumerate(thrindli)]
    yli = [yvec[i][ind] for i, ind in enumerate(thrindli)]
    plt.plot(xli, yli, 'o', **kwargs)


def plot_traj_thresh(indir, xname, yname):
    with open(os.path.join(indir, 'fifos.p')) as f:
        fifos = pickle.load(f)
    runpar = jspar.load(os.path.join(indir, 'runpar.json'))
    fifo_trange = runpar['fifo_trange']
    dt = runpar['hpar']['dt']
    trng = (-40, -0.05)
    plot_traj(fifos, xname, yname, trng, fifo_trange, dt)
    plot_thresh(fifos, xname, yname, iname='icap_ais', ithresh=0.001)


def plot_timetraj_thresh(indir, yname, tname='time'):
    with open(os.path.join(indir, 'recs.p')) as f:
        recs = pickle.load(f)
    plt.plot(recs[tname], recs[yname])
    with open(os.path.join(indir, 'fifos.p')) as f:
        fifos = pickle.load(f)
    plot_thresh(fifos, tname, yname, iname='icap_ais', ithresh=0.001)

def plot_align_thresh(indir, yname, trajcolor, thrcolor, label= '', tname='time'):
    with open(os.path.join(indir, 'fifos.p')) as f:
        fifos = pickle.load(f)
    runpar = jspar.load(os.path.join(indir, 'runpar.json'))
    fifo_trange = runpar['fifo_trange']
    dt = runpar['hpar']['dt']
    trng = (-20, -0.05)
    taname = 'time_align'
    fifos[taname] = np.tile(np.arange(fifo_trange[0], fifo_trange[1], dt), (len(fifos[yname]), 1))
    plot_traj(fifos, taname, yname, trng, fifo_trange, dt, label=label, color=trajcolor, alpha=0.7)
    plot_thresh(fifos, taname, yname, iname='icap_ais', ithresh=0.001, color=thrcolor, label=label+' thresh', alpha=0.7)


if __name__ == '__main__':
    optdir = '../../results/BSNaKResetNew/opt_stimpar'
    threxdir = '../../figures/BSNaKResetNew/threshold_example'

    ttime = 10000
    recnames = ('time', 'v_ais', 'icap_ais', 'nav_m')
    fifonames = ('time', 'v_ais', 'icap_ais', 'nav_m')
    fifo_trange = (-40, 0)

    tau = 30
    frttarg = 5
    cvtarg = 1.
    tfcsubdir = labeldir.opt_subdir(tau, frttarg, cvtarg)
    optsubdir = os.path.join(optdir, tfcsubdir)
    threxsubdir = os.path.join(threxdir, tfcsubdir)

    # gkbar = 0
    # gkdir = labeldir.gkbar_dir(gkbar)
    # outdir = os.path.join(threxsubdir, gkdir)
    # # plot_traj_thresh(outdir, 'time', 'nav_m')
    # plot_align_from_file(outdir, 'nav_m')
    # plt.show()
    
    gkbarli = [0, 5e-3, 15e-3]
    trajcolorli = ['#1f77b4', '#ff7f0e', '#2ca02c']
    thrcolorli = ['darkblue', 'chocolate', 'darkgreen']

    for i, gkbar in enumerate(gkbarli):
        trajcolor = trajcolorli[i]
        thrcolor = thrcolorli[i]
        gkdir = labeldir.gkbar_dir(gkbar)
        outdir = os.path.join(threxsubdir, gkdir)
        # plot_traj_thresh(outdir, 'time', 'nav_m')
        gklab = labeldir.gkbar_lab(gkbar)
        plot_align_thresh(outdir, 'nav_m', trajcolor, thrcolor, label=gklab)
    plt.xlabel('time to spike (ms)')
    plt.ylabel('Nav gating variable $m$')
    plt.legend()
    plt.savefig(os.path.join(threxsubdir, 'mt.pdf'))
    plt.show()
