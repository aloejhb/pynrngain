import numpy as np
from math import exp, sqrt, pi
"""
Functions for Ornstein-Uhlenbeck process
"""

def ou_vec(mean, std, tau, ttime, dt, rseed=None):
    """
    Return a vector of OU process
    Arguments:
    mean, std, tau: parameters of OU process
    ttime: total time of OU process
    dt: time interval in each time step
    rseed: seed for random number generator
    Returns:
    vec: vector of a realization of OU process
    """
    if std <= 0:
        raise ValueError('std <= 0')
    
    if rseed:
        np.random.seed(rseed)

    vec = []
    vec.append(np.random.normal(mean, std))

    for i in range(int(ttime/dt)):
        v = vec[-1] + (1 - exp(-dt/tau)) * (mean - vec[-1]) + sqrt(1 - exp(-2*dt/tau))*std*np.random.normal(0, 1)
        vec.append(v)

    return np.array(vec)


def ou_make_psd(mean, std, tau):
    """
    Function wrapper for power spectral density(PSD) of an OU process
    Arguments:
    mean, std, tau: parameters of OU process
    Returns:
    ou_psd: vectorized function to calculate PSD at certain frequency f
    """
    tau = tau * 1e-3  # convert tau unit from ms to s

    def ou_psd(f):
        psd = 2*tau*(std**2)/(1+(2*pi*tau*f)**2)
        return psd

    return np.vectorize(ou_psd)
