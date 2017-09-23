import logging
import numpy as np
from scipy.optimize import minimize_scalar
from .spkstat import cut_spktimes, firing_rate, cv_isi, lv_isi
from . import jspar


def targfunc_wrapper(simfunc, xname, tau, statname, targ, ttime,
                     rseed=None, cstart=500., simargs=()):

    if ttime < cstart:
        raise ValueError('Total time less than cut start time!')

    if xname not in ('std', 'mean'):
        raise ValueError('xname {} not valid! Should be either std or mean'.format(xname))

    if statname not in ('frt', 'cv', 'lv'):
        raise ValueError('{} is not a valid statistics name. Should be frt, cv or lv'.format(statname))

    def targfunc(x, fx):
        logging.info('x0: ' + str(x))

        if xname == 'std' and x <= 0:
            logging.info('Std less than zero!')
            return 1e10

        if xname == 'std':
            stimpar = {'mean': fx, 'std': x, 'tau': tau}
        elif xname == 'mean':
            stimpar = {'mean': x, 'std': fx, 'tau': tau}
        else:
            raise ValueError('xname {} not valid! Should be either std or mean'.format(xname))

        spktimes = simfunc(ttime, 'OU', stimpar, rseed, *simargs)
        cutspkt = cut_spktimes(spktimes, cstart)

        if statname == 'frt':
            frt = firing_rate(cutspkt, ttime-cstart)
            res = (frt - targ)**2 / targ**2
            logging.info('f:{0:.2f}\tr:{1:.6f}'.format(frt, res))
        elif statname == 'cv':
            if len(cutspkt) < 2:
                logging.info('Less than two spikes!')
                res = 1e9
                logging.info('c:{0:.6f}\tr:{1:.6f}'.format(np.nan, res))
            else:
                cv = cv_isi(cutspkt)
                res = (cv - targ)**2 / targ**2
                logging.info('c:{0:.6f}\tr:{1:.6f}'.format(cv, res))
        elif statname == 'lv':
            if len(cutspkt) < 2:
                logging.info('Less than two spikes!')
                res = 1e9
                logging.info('l:{0:.6f}\tr:{1:6f}'.format(np.nan, res))
            else:
                lv = lv_isi(cutspkt)
                res = (lv - targ)**2 / targ**2
                logging.info('l:{0:.6f}tr:{1:.6f}'.format(lv, res))
        else:
            raise ValueError('{} is not a valid statistics name. Should be frt, cv or lv'.format(statname))

        return res

    return targfunc


def get_contour(targfunc, fxvec, bracket, funtol=1e-3):

    logging.info('Start estimating contour!')
    xvec = []
    for fx in fxvec:
        logging.info('fx: %f' % fx)
        res = minimize_scalar(targfunc, bracket=bracket, args=(fx,), method='Brent', options={'maxiter': 50})
        logging.info(str(res))
        if res.fun < funtol:
            xvec.append(res.x)
        else:
            xvec.append(np.nan)

    return np.array(xvec)


if __name__ == '__main__':
    pass
    # rseed = 3
    # targfunc = targfunc_wrapper(simfunc, *args, **kwargs)
