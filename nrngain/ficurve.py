import numpy as np
from .spkstat import (cut_spktimes, firing_rate)


def get_frtvec(simfunc, curtvec, noise=0, tau=5., args=(), dur=3000, delay=100, cutt=200):
    if dur < 2 * cutt:
        raise ValueError('Stimulus duration should be lager than twice the cut time!')

    # XXXXX noiseA
    ttime = delay + dur
    cstart = delay + cutt
    cend = ttime - cutt

    frtvec = []

    for cur in curtvec:
        if noise:
            stimtyp = 'OU'
            stimpar = {'mean': cur, 'std': noise, 'tau': tau}
        else:
            stimtyp = 'step'
            stimpar = {'amp': cur, 'dur': dur, 'delay': delay}
        spktimes = simfunc(ttime, stimtyp, stimpar, *args)
        cutspkt = cut_spktimes(spktimes, cstart, cend)
        frate = firing_rate(cutspkt, cend - cstart)
        frtvec.append(frate)

    return frtvec


def fire_thresh_i(curtvec, frtvec, frt_targ=0):
    ind = np.where(frtvec > frt_targ)[0][0]
    return curtvec[ind], frtvec[ind]


if __name__ == '__main__':
    pass
