import os
import neuron

from .stimulus import create_stim
from .recording import (create_recordings, recordings_to_dict)
from .spikecount import create_spkcount
from .pyfifo import (create_fifos, pyfifos_to_dict)


def initiation(ttime, hpar=None):
    """Initialize simulation environment"""
    print('Initializing simulation')
    neuron.h.load_file('nrngui.hoc')
    # neuron.load_mechanisms(mecpath)
    neuron.h.cvode_active(0)
    neuron.h.tstop = ttime
    if hpar:
        neuron.h.dt = hpar['dt']
        neuron.h.celsius = hpar['celsius']


def par_to_list(par, order):
    parli = [par[o] for o in order]
    return parli


def create_cell(modelfile, cellpar, cporder):
    if os.path.isfile(modelfile):
        neuron.h.load_file(modelfile)
        cpli = par_to_list(cellpar, cporder)
        cell = neuron.h.Cell(*cpli)
    else:
        raise IOError('Cannot open model template file. %s' % modelfile)
    return cell
