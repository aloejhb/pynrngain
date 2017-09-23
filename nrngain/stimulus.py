import neuron
import numpy as np
from .ouprocess import ou_vec


def create_stim(nrnobj, typ, par, rseed=None):
    """
    Create current clamp stimulus
    input:
        nrnobj: NEURON object where stimulus is applied
        typ: stimulus type
             'step': step stimulus
             'OU': Ornstein-Uhlenberck process
        par: dictionary containing stimulus parameters
             step: {dur, delay, amp}
             OU: {mean, std, tau}
    """
    iclamp = neuron.h.IClamp(nrnobj)

    if typ == 'step':
        iclamp.dur = par['dur']
        iclamp.delay = par['delay']
        iclamp.amp = par['amp']
        ivec = None
    elif typ == 'OU':
        iclamp.dur = neuron.h.tstop + 1
        iclamp.delay = 0
        iclamp.amp = 0
        mean = par['mean']
        std = par['std']
        tau = par['tau']
        if std == 0:
            iclamp.amp = mean
            ivec = np.ones(int(iclamp.dur/neuron.h.dt)) * mean
        else:
            ouvec = ou_vec(mean, std, tau, neuron.h.tstop, neuron.h.dt, rseed)
            ivec = neuron.h.Vector()
            ivec.from_python(ouvec)
            ivec.play(iclamp._ref_amp, neuron.h.dt)
    else:
        raise ValueError('Not correct stiumulus type! Use: step, OU or sinnoise')

    return iclamp, ivec
