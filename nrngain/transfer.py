import math
import numpy as np
from scipy import signal
from .ouprocess import ou_make_psd


def trapezoid_window(M, sdratio=0.0625):
    """Return a trapezoid window, with M points"""
    sdlen = int(M*sdratio)
    side = np.linspace(0, 1, sdlen)
    window = np.concatenate((side, np.ones(M-2*sdlen), 1-side))
    return window


def windowing(sig):
    """Multiply signal with a window function"""
    M = len(sig)
    # window = trapezoid_window(M)
    window = np.hamming(M)
    wsig = sig * window
    return wsig


def smooth(x, window_std=1., window_len=11):
    """Smooth data by convolving with a Gaussian window function"""
    if window_len < 3:
        return x

    s = np.r_[x[window_len-1:0:-1], x, x[-1:-window_len:-1]]
    w = signal.gaussian(window_len, window_std)

    y = np.convolve(w/w.sum(), s, mode='valid')
    y = y[window_len/2: -window_len/2+1]
    return y


def smooth_strong_high_freq(ft, fvec):
    """
    Special smoothing function for Fourier transform result
    Stronger smoothing for higher frequency
    """
    if len(ft) != len(fvec):
        raise ValueError('FT result and frequency vector should have the same length!')

    flen = len(ft)
    sft = np.zeros(flen, dtype=complex)

    for i in range(flen):
        if i == 0:
            g = np.zeros(flen)
            g[0] = 1
        else:
            g = math.e**(-2*math.pi**2*(fvec-fvec[i])**2/fvec[i]**2)
            g = g/float(sum(g))
        sft[i] = sum(ft*g)

    return sft


def fft_sta(sta, dt, maxfreq, sm):
    nsta = len(sta)

    # Windowing of signal to minimize spectral leakage in FFT
    wsta = windowing(sta)

    # Shift starting time point to the spike time
    # by rolling the sta array to the middle
    swsta = np.roll(wsta, len(wsta)/2)

    # Do Fast Fourier Transform
    ftsta = np.fft.fft(swsta)
    fvec = np.fft.fftfreq(nsta, d=dt)

    # Cut resulting vector to max frequency
    sfreq = 1/dt
    maxf_ind = int(nsta * maxfreq/sfreq)
    ftsta = np.roll(ftsta, -1)[:nsta/2]
    ftsta = ftsta[:maxf_ind]
    fvec = fvec[:maxf_ind]

    if sm == 'Gaussian':
        ftsta = smooth(ftsta, window_std=5.)
    elif sm == 'Gauss-strong-high-freq':
        ftsta = smooth_strong_high_freq(ftsta, fvec)

    return ftsta, fvec


def get_transfer(sta, stimpar, dt, frt, maxfreq=500):

    ftsta, fvec = fft_sta(sta, dt, maxfreq, sm='Gauss-strong-high-freq')

    ou_psd = ou_make_psd(**stimpar)
    psd = ou_psd(fvec)
    transf = np.divide(ftsta, psd) * frt *1e-3 # firing rate in unit ms^-1

    return transf, ftsta, psd, fvec


def get_cutoff_freq(fvec, gain, ind=False):
    """
    Return cutoff frequency of a filter gain
    """
    if len(fvec) != len(gain):
        raise ValueError('gain and freqeuncy vec should be the same length!')
    cogain = gain[1]/np.sqrt(2)
    coind = np.where(np.diff(np.sign(gain - cogain))<0)[0][0]
    if ind:
        return coind, fvec[coind], gain[coind]
    return fvec[coind]


def run_transfer(indir):
    import os
    from .jspar import load as jsload
    spkstat = jsload(os.path.join(indir, 'spkstat.json'))
    frt = spkstat['frt']
    runpar = jsload(os.path.join(indir, 'runpar.json'))
    dt = runpar['hpar']['dt']
    stimpar = runpar['stimpar']

    sta = np.load(os.path.join(indir, 'sta.npy'))
    maxtau = len(sta)/2 * dt
    tauvec = np.linspace(-maxtau, maxtau, len(sta))
    
    transf, ftsta, psd, fvec = get_transfer(sta, stimpar, dt*1e-3, frt) # transform unit of dt from (ms) to (s)

    outdir = os.path.join(indir, 'transfer')

    if not os.path.exists(outdir):
        os.mkdir(outdir)
        
    np.save(os.path.join(outdir, 'transf.npy'), transf)
    np.save(os.path.join(outdir, 'ftsta.npy'), ftsta)
    np.save(os.path.join(outdir, 'psd.npy'), psd)
    np.save(os.path.join(outdir, 'fvec.npy'), fvec)


if __name__ == '__main__':
    pass
