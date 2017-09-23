import neuron

import sys
sys.path.append('../../')
from nrngain import sim

modelfile = 'template.hoc'

hpar = {'dt':      0.025,
        'celsius': 25.}

cporder = ('pos_ais', 'gnabar', 'gkbar', 'ap_thresh')


def get_reddef(cell, recnames):
    pos_ais = cell.get_pos_ais()
    recdict = {'time':   neuron.h._ref_t,
               'v_ais':  cell.axon(pos_ais)._ref_v,
               'icap_ais': cell.axon(pos_ais)._ref_i_cap,
               'ina':    cell.axon(pos_ais)._ref_ina,
               'nav_m': cell.nav._ref_m}
    if hasattr(cell, 'kv') and cell.kv:
        recdict.update({'ik':     cell.axon(pos_ais)._ref_ik,
                        'kv_n':   cell.kv._ref_n})
    recdef = {k: recdict[k] for k in recnames}
    return recdef


def overwrite_advance():
    if len(neuron.h.fifolist):
        neuron.h('''
          proc advance() {
              fadvance()
              Cell[0].check_reset()
              fifo_advance(fifospkc)
          }
        ''')
    else:
        neuron.h('''
          proc advance() {
              fadvance()
              Cell[0].check_reset()
          }
        ''')


def simulation(cellpar, spkthr, ttime, stimtyp, stimpar, rseed=None,
               retstim=False, recnames=None, fifonames=None, fifo_trange=None):
    sim.initiation(ttime, hpar)
    cell = sim.create_cell(modelfile, cellpar, cporder)
    if stimtyp:
        stim, stimvec = sim.create_stim(cell.soma(0.5), stimtyp, stimpar, rseed)
    spkcount, spktimes = sim.create_spkcount(cell.axon, cell.get_pos_ais(), spkthr)

    if recnames:
        recdef = get_reddef(cell, recnames)
        recordings = sim.create_recordings(recdef)

    if fifonames:
        ffdef = get_reddef(cell, fifonames)
        pyfifos = sim.create_fifos(ffdef, fifo_trange, spkcount)

    overwrite_advance()
    neuron.h.run()

    res = [spktimes]

    if retstim:
        res.append(stimvec)
    if recnames:
        res.append(recordings)
    if fifonames:
        fifos = sim.pyfifos_to_dict(pyfifos)
        res.append(fifos)
        
    return tuple(res)


def cellpar_wrapper(simfunc, cellpar, spkthr):

    def cellpar_simfunc(*args, **kwargs):
        return simfunc(cellpar, spkthr, *args, **kwargs)

    return cellpar_simfunc


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    import nrngain.recording as rcd
    import nrngain.spkstat as spst

    
    ttime = 1500.
    cellpar = {'pos_ais': 0.1,
               'gnabar': 0.001,
               'gkbar': 0.000,
               'ap_thresh': -40}
    spkthr = -40
    stimtyp = 'step'
    stimpar = {'dur': 1000., 'delay': 400., 'amp': 0.07}
    # stimtyp = 'OU'
    # stimpar = {'mean': 0.03, 'std': 0.08, 'tau': 5}
    # stimtyp = None
    # stimpar = None

    recnames = ('time', 'v_ais')#, 'nav_m')
    spkt, recs = simulation(cellpar, spkthr, ttime, stimtyp, stimpar, None, recnames=recnames)
    # print np.array(spkt)
    stimtime = stimpar['dur']
    frt, cv, lv = spst.get_spkstat(spkt, stimtime)
    print 'f:{}\tc:{}\tl:{}'.format(frt, cv, lv)
    rcd.plot_recordings(recs)
    plt.show()
