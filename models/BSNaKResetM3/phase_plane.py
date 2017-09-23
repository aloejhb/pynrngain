import os
import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt
import run
sys.path.append('../../')
import nrngain.phaseplane as pp
import nrngain.pyfifo as pff

cellpar = {'pos_ais': 0.1,
           'gnabar': 0.005,
           'gkbar': 0,
           'ap_thresh': -40}
spkthr = -40

simfunc = run.cellpar_wrapper(run.simulation, cellpar, spkthr)
# cur = 0.05
# pp.plot_const_stim_traj(simfunc, cur, ('v', 'icap'))
# plt.show()

ttime = 2000
stimpar = {'mean': 0.1, 'std': 0.1, 'tau': 20}
fifonames = ('time', 'v_ais', 'icap_ais')
fifo_trange = (-40, 0)

figdir = '../../figures/BSNaKResetM3/'
ppdir = os.path.join(figdir, 'phase_plane')
outdir = os.path.join(ppdir, 'tmp')

spkt, pyfifos = simfunc(ttime, 'OU', stimpar, None,
                        fifonames=fifonames, fifo_trange=fifo_trange)
fifos = pff.pyfifos_to_dict(pyfifos)
# pff.save_fifos(pyfifos, outdir)


# fffile = os.path.join(outdir, 'fifos.p')
# with open(fffile) as f:
#     fifos = pickle.load(f)

dt = run.hpar['dt']
trng = (-1, -0.05)
def get_ffind(t, ffstart, dt):
    return int((t-ffstart) / dt)
rng = map(lambda x: get_ffind(x, fifo_trange[0], dt), trng)
print rng
print len(fifos['v_ais'][0])
pp.plot_multi_traj(fifos['v_ais'], fifos['icap_ais'], fir=0, num=20, rng=rng,
                   vnames=('v_ais', 'icap_ais'), units=None, label=None)
plt.show()
