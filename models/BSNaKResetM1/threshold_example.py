import os
import pickle
import matplotlib.pyplot as plt
import labeldir
import threshold
import run
import sys
sys.path.append('../..')
from nrngain import jspar
import nrngain.phaseplane as pp


def run_recs_fifos(pardir, outdir, ttime, recnames, fifonames, fifo_trange):
    stimpar = jspar.load(os.path.join(pardir, 'stimpar.json'))
    cellpar = jspar.load(os.path.join(pardir, 'cellpar.json'))
    spkthr = jspar.load(os.path.join(pardir, 'spkthr.json'))

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    simfunc = run.cellpar_wrapper(run.simulation, cellpar, spkthr)
    spkt, stimvec, recs, fifos = simfunc(ttime, 'OU', stimpar, None, retstim=True, recnames=recnames, fifonames=fifonames, fifo_trange=fifo_trange)

    with open(os.path.join(outdir, 'fifos.p'), 'w') as f:
        pickle.dump(fifos, f)
    with open(os.path.join(outdir, 'recs.p'), 'w') as f:
        pickle.dump(recs, f)
    runpar = dict(hpar=run.hpar,
                  ttime=ttime,
                  stimpar=stimpar,
                  cellpar=cellpar,
                  spkthr=spkthr,
                  fifo_trange=fifo_trange)
    rpfile = os.path.join(outdir, 'runpar.json')
    jspar.save(rpfile, runpar)


def get_ffind(t, ffstart, dt):
    return int((t-ffstart) / dt)


def get_var_at_thresh(fifos, thrindli, varname):
    return [fifos[varname][i][ind] for i, ind in enumerate(thrindli)]


def plot_v_time_thresh(indir, figpath, ithresh=0.001):
    plt.figure()
    with open(os.path.join(indir, 'recs.p')) as f:
        recs = pickle.load(f)
    plt.plot(recs['time'], recs['v_ais'])

    with open(os.path.join(indir, 'fifos.p')) as f:
        fifos = pickle.load(f)
    thrindli = map(lambda x: threshold.find_thresh_ind(x, ithresh), fifos['icap_ais'])
    thrlis = {}
    thrlis['time'] = get_var_at_thresh(fifos, thrindli, 'time')
    thrlis['v_ais'] = get_var_at_thresh(fifos, thrindli, 'v_ais')
    plt.plot(thrlis['time'], thrlis['v_ais'], 'ok')
    plt.xlim((-100, 6000))
    plt.xlabel('time (ms)')
    plt.ylabel('AIS membrane voltage (mV)')
    plt.tight_layout()
    plt.savefig(figpath)


def plot_i_v_thresh(indir, figpath, ithresh=0.001):
    plt.figure()
    with open(os.path.join(indir, 'fifos.p')) as f:
        fifos = pickle.load(f)
    runpar = jspar.load(os.path.join(indir, 'runpar.json'))
    fifo_trange = runpar['fifo_trange']
    dt = runpar['hpar']['dt']
    # trng = (-1, -0.05)
    trng = (-20, -0.05)
    rng = map(lambda x: get_ffind(x, fifo_trange[0], dt), trng)
    pp.plot_multi_traj(fifos['v_ais'], fifos['icap_ais'], fir=15, num=20, rng=rng, color='#1f77b4', alpha=0.7)
    plt.axhline(ithresh, color='k', linestyle='dashed')
    plt.xlabel('AIS membrane voltage (mV)')
    plt.ylabel('AIS current density(mA/cm$^2$)')
    plt.tight_layout()
    plt.savefig(figpath)


def plot_m_v(indir, label, trajcolor):
    with open(os.path.join(indir, 'fifos.p')) as f:
        fifos = pickle.load(f)
    runpar = jspar.load(os.path.join(indir, 'runpar.json'))
    fifo_trange = runpar['fifo_trange']
    dt = runpar['hpar']['dt']
    # trng = (-1, -0.05)
    trng = (-20, -0.05)
    rng = map(lambda x: get_ffind(x, fifo_trange[0], dt), trng)
    pp.plot_multi_traj(fifos['v_ais'], fifos['nav_m'], fir=0, num=20, rng=rng, label=label, color=trajcolor, alpha=0.5)


def plot_m_v_thresh(indir, label, thrcolor):
    with open(os.path.join(indir, 'fifos.p')) as f:
        fifos = pickle.load(f)
    thrindli = map(threshold.find_thresh_ind, fifos['icap_ais'])
    thrlis = {}
    thrlis['v_ais'] = get_var_at_thresh(fifos, thrindli, 'v_ais')
    thrlis['nav_m'] = get_var_at_thresh(fifos, thrindli, 'nav_m')

    plt.plot(thrlis['v_ais'], thrlis['nav_m'], 'o', color=thrcolor, label=label+' thresh', alpha=0.5)

    
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

    gkbar = 0
    gkdir = labeldir.gkbar_dir(gkbar)
    outdir = os.path.join(threxsubdir, gkdir)
    vtfigpath = os.path.join(threxsubdir, 'vt_'+gkdir+'.pdf')
    ivfigpath = os.path.join(threxsubdir, 'iv_'+gkdir+'.pdf')
    plot_v_time_thresh(outdir, vtfigpath)
    plot_i_v_thresh(outdir, ivfigpath)
    plt.show()

    # gkbarli = [0, 5e-3, 15e-3]
    # trajcolorli = ['#1f77b4', '#ff7f0e', '#2ca02c']
    # thrcolorli = ['darkblue', 'chocolate', 'darkgreen']

    # from channel_prop import get_navvecs
    # import numpy as np
    # vvec = np.linspace(-70, -40)
    # navvecs = get_navvecs(vvec)
    # plt.plot(vvec, navvecs['minf'], label='$m_{\inf}$', color='k', linewidth=5, linestyle='dashed', alpha=0.3)
    
    # for i, gkbar in enumerate(gkbarli):
    #     gkdir = labeldir.gkbar_dir(gkbar)
    #     pardir = os.path.join(optsubdir, gkdir)
    #     outdir = os.path.join(threxsubdir, gkdir)
    #     if not os.path.exists(outdir):
    #         os.makedirs(outdir)
    #     # run_recs_fifos(pardir, outdir, ttime, recnames, fifonames, fifo_trange)
    #     gklab = labeldir.gkbar_lab(gkbar)
    #     trajcolor = trajcolorli[i]
    #     plot_m_v(outdir, gklab, trajcolor)
    # for i, gkbar in enumerate(gkbarli):
    #     gkdir = labeldir.gkbar_dir(gkbar)
    #     outdir = os.path.join(threxsubdir, gkdir)
    #     gklab = labeldir.gkbar_lab(gkbar)
    #     thrcolor = thrcolorli[i]
    #     plot_m_v_thresh(outdir, gklab, thrcolor)

    # plt.xlabel('AIS membrane voltage (mV)')
    # plt.ylabel('Nav gating variable $m$')
    # plt.legend()
    # plt.savefig(os.path.join(threxsubdir, 'mv.pdf'))
    # plt.show()

    # indir = os.path.join(ppsubdir, gkdir)
    # with open(os.path.join(indir, 'fifos.p')) as f:
    #     fifos = pickle.load(f)
    # runpar = jspar.load(os.path.join(indir, 'runpar.json'))
    # dt = runpar['hpar']['dt']
    # fifo_trange = runpar['fifo_trange']

    # # trng = (-1, -0.05)
    # trng = (-40, -0.05)

    # rng = map(lambda x: get_ffind(x, fifo_trange[0], dt), trng)
    # # pp.plot_multi_traj(fifos['v_ais'], fifos['icap_ais'], fir=0, num=20, rng=rng,
    # #                    vnames=('v_ais', 'icap_ais'), units=None, label=None)
    # pp.plot_multi_traj(fifos['time'], fifos['v_ais'], fir=0, num=20, rng=rng,
    #                    vnames=('time', 'v_ais'), units=None, label=None)
    # plt.show()
