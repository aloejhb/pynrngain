import os
import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt
import run
import labeldir
sys.path.append('../../')
import nrngain.jspar as jspar
import nrngain.phaseplane as pp
import nrngain.pyfifo as pff


def run_fifos(ttime, pardir, outdir):
    stimpar = jspar.load(os.path.join(pardir, 'stimpar.json'))
    cellpar = jspar.load(os.path.join(pardir, 'cellpar.json'))
    spkthr = jspar.load(os.path.join(pardir, 'spkthr.json'))

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    simfunc = run.cellpar_wrapper(run.simulation, cellpar, spkthr)

    fifonames = ('time', 'v_ais', 'icap_ais', 'nav_m')
    fifo_trange = (-40, 0)

    spkt, fifos = simfunc(ttime, 'OU', stimpar, None,
                          fifonames=fifonames, fifo_trange=fifo_trange)
    pff.save_fifos(fifos, outdir)
    runpar = dict(hpar=run.hpar,
                  ttime=ttime,
                  stimpar=stimpar,
                  cellpar=cellpar,
                  spkthr=spkthr,
                  fifo_trange=fifo_trange)
    rpfile = os.path.join(outdir, 'runpar.json')
    jspar.save(rpfile, runpar)


if __name__ == '__main__':

    ppdir = '../../figures/BSNaKResetNew/phase_plane'
    optdir = '../../results/BSNaKResetNew/opt_stimpar'

    tauli = [5, 30]
    frttargli = [5, 10]
    gkbarli = [0, 5e-3, 15e-3]
    ttime = 20000

    for tau in tauli:
        for frttarg in frttargli:
            cvtarg = 1.
            optsubdir = labeldir.opt_subdir(tau, frttarg, cvtarg)

            for gkbar in gkbarli:
                gkdir = labeldir.gkbar_dir(gkbar)
                pardir = os.path.join(optdir, optsubdir, gkdir)
                outdir = os.path.join(ppdir, optsubdir, gkdir)
                run_fifos(ttime, pardir, outdir)



# cellpar = {'pos_ais': 0.1,
#            'gnabar': 0.005,
#            'gkbar': 0,
#            'ap_thresh': -40}
# spkthr = -40

# cur = 0.05
# pp.plot_const_stim_traj(simfunc, cur, ('v', 'icap'))
# plt.show()
# gkbar = 0
# gkdir = labeldir.gkbar_dir(gkbar)
# outdir = os.path.join(ppdir, optsubdir, gkdir)

# fifo_trange = (-40, 0)

# fffile = os.path.join(outdir, 'fifos.p')
# with open(fffile) as f:
#     fifos = pickle.load(f)

# dt = run.hpar['dt']
# # trng = (-1, -0.05)
# trng = (-40, -0.05)
# def get_ffind(t, ffstart, dt):
#     return int((t-ffstart) / dt)
# rng = map(lambda x: get_ffind(x, fifo_trange[0], dt), trng)
# print rng
# print len(fifos['v_ais'][0])
# pp.plot_multi_traj(fifos['v_ais'], fifos['icap_ais'], fir=0, num=20, rng=rng,
#                    vnames=('v_ais', 'icap_ais'), units=None, label=None)
# # pp.plot_multi_traj(fifos['v_ais'], fifos['nav_m'], fir=0, num=20, rng=rng,
# #                    vnames=('v_ais', 'nav_m'), units=None, label=None)
# plt.show()
