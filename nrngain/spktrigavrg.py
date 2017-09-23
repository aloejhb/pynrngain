import numpy as np

"""Python script to calculate spike-trigged-average (STA)"""

"""
 * @file spktrigavrg.py
 * @brief Function for calculating spike-triggered-average
 * @author Bo Hu
 * @date 2016
"""


def cut_stim(stim, spt, maxtau, dt):
    stind = int((spt-maxtau) / dt)
    edind = int((spt+maxtau) / dt)
    return stim[stind:edind]


def get_sta(stim, spktimes, maxtau, dt, stim_mean):
    """
    Arguments:
    * stim: vector of stimulus
    * spktimes: vector of spike time
    * maxtau: maximum tau value for spike-triggered-average
    * dt: length of each time step, corresponding to each point in stim
    * stim_mean: mean value of stimulus

    Returns:
    * sta: spike-triggered-average
    """

    stim = np.array(stim)
    spk_trig_stim = []
    for spt in spktimes:
        if spt > maxtau and spt < (len(stim)*dt-maxtau):
            # cutout spikes at the first and last maxtau,
            # which have incomplete stim
            cstim = cut_stim(stim, spt, maxtau, dt)
            spk_trig_stim.append(cstim)
    if not spk_trig_stim:
        raise Exception('No spike between maxtau and total time - maxtau!')
    spk_trig_stim = np.array(spk_trig_stim)
    sta = np.average(spk_trig_stim, axis=0)

    sta = sta - stim_mean

    return sta


def sta_tauvec(maxtau, dt):
    tauvec = np.arange(-maxtau, maxtau, dt)
    return tauvec


def combine_sta(sta_list, nspk_list):

    if len(sta_list) != len(nspk_list):
        raise ValueError('For each STA, total number of spikes should be provided!')

    stamat = np.array(sta_list)

    if stamat.dtype == 'O':
        raise ValueError('All STAs should have the same length')

    csta = np.average(stamat, axis=0, weights=nspk_list)

    return csta


if __name__ == '__main__':
    pass
