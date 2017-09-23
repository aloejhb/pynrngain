import numpy as np
import os
from . import jspar


def cut_spktimes(spktimes, start, end=None):
    spktimes = np.array(spktimes)

    if end is None:
        cutind = np.where(spktimes > start)
    else:
        cutind = np.where((spktimes > start) & (spktimes < end))

    return spktimes[cutind]


def firing_rate(spktimes, ttime):
    ttime_sec = ttime * 1e-3  # Convert time unit into second
    frate = len(spktimes)/ttime_sec
    return frate


def cv_isi(spktimes):
    spktimes = np.array(spktimes)
    if len(spktimes) < 3:
        return np.nan
    isi = np.diff(spktimes)
    std = np.std(isi)
    mean = np.mean(isi)
    cv = std/mean
    return cv


def lv_isi(spktimes):
    spktimes = np.array(spktimes)
    if len(spktimes) < 3:
        return np.nan
    isi = np.diff(spktimes)
    risi = np.roll(isi, 1)
    llv = map(lambda x, y: ((x-y)/(x+y))**2, risi[1:], isi[1:])
    lv = np.mean(llv) * 3
    return lv


def get_spkstat(spktimes, ttime, cstart=0):
    cutspkt = cut_spktimes(spktimes, cstart)
    frt = firing_rate(cutspkt, ttime)
    cv = cv_isi(cutspkt)
    lv = lv_isi(cutspkt)
    return frt, cv, lv


def get_spkstat_from_file(indir, cstart=0):
    spktimes = np.load(os.path.join(indir, 'spktimes.npy'))
    runpar = jspar.load(os.path.join(indir, 'runpar.json'))
    ttime = runpar['ttime']
    frt, cv, lv = get_spkstat(spktimes, ttime, cstart)
    spkstat = {'frt': frt, 'cv': cv, 'lv': lv}
    spkstatfile = os.path.join(indir, 'spkstat.json')
    jspar.save(spkstatfile, spkstat)


if __name__ == '__main__':
    spktimes = [1, 5, 6, 10, 12, 20, 21]
    frt, cv, lv = get_spkstat(spktimes, spktimes[-1])
    print frt, cv, lv
