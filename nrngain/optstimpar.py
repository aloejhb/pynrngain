import logging
from datetime import datetime
import numpy as np
from scipy.optimize import minimize

from .spkstat import (cut_spktimes, firing_rate, cv_isi)


def scaled_sqrtres(yv, yvtarg):
    """Return the scaled square residue of vector.

    >>> scaled_sqrtres((2, 4), (1, 2))
    2
    """
    resv = map(lambda a: ((a[0]-a[1])/a[1])**2, zip(yv, yvtarg))
    return sum(resv)


def targfunc_wrapper(simfunc, tau, ttime, frttarg, cvtarg,
                     rseed=None, simargs=(), cstart=2000.):
    if ttime < cstart:
        raise ValueError('Total time less than cut start time!')

    def targfunc(x):

        logging.info('x0: ' + str(x))

        if x[1] < 0:
            logging.info('std less than zero!')
            return 1e10

        stimpar = {'mean': x[0],
                   'std': x[1],
                   'tau': tau}

        spktimes = simfunc(ttime, 'OU', stimpar, rseed, *simargs)
        cutspkt = cut_spktimes(spktimes, cstart)

        if len(cutspkt) < 2:
            logging.info('Less than 2 spikes, cannot calculate CV!')
            frt = np.nan
            cv = np.nan
            res = 1e9
        else:
            frt = firing_rate(cutspkt, ttime-cstart)
            cv = cv_isi(cutspkt)
            res = scaled_sqrtres((frt, cv), (frttarg, cvtarg))

        logging.info('f:%.2f\tc:%.4f\tr:%.6f' % (frt, cv, res))

        return res

    return targfunc


def optstimpar(simfunc, x0, tau, ttime, frttarg, cvtarg,
               rseed=None, simargs=()):

    logging.info('--------------------------------------------')

    logging.info('Optimizing OU stimulus parameters')
    logging.info('frttarg:%.2f\tcvtarg:%.2f' % (frttarg, cvtarg))

    if rseed is None:
        rseed = datetime.now().microsecond

    targfunc = targfunc_wrapper(simfunc, tau, ttime,
                                frttarg, cvtarg, rseed, simargs)

    # TODO limit number of iteration and precision
    res = minimize(targfunc, x0, method='Nelder-Mead',
                   options={'maxiter': 200})
    logging.info(str(res))

    # TODO check if minimize succeeded
    ostimpar = {'mean': res.x[0],
                'std': res.x[1],
                'tau': tau}

    return ostimpar, res


if __name__ == '__main__':
    import doctest
    doctest.testmod()
