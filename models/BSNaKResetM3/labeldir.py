import os


def gkbar_lab(gkbar):
    if gkbar:
        return '$\\bar{g}_K =$ %.1f nS' % (gkbar*1e3)
    return 'w/o Kv'


def gkbar_dir(gkbar):
    return 'gk{:.0f}'.format(gkbar*1e3).replace('.', '-')


def tau_dir(tau):
    return 'tau{:.0f}'.format(tau)


def tau_lab(tau):
    return '$\\tau =$ {:.0f}ms'.format(tau)


def targs_dir(frttarg, cvtarg):
    sdir = 'frt{:.0f}_cv{:.1f}'.format(frttarg, cvtarg)
    return sdir.replace('.', '-')


def opt_subdir(tau, frttarg, cvtarg):
    taudir = tau_dir(tau)
    targsdir = targs_dir(frttarg, cvtarg)
    return os.path.join(taudir, targsdir)


def opt_path(tau, frttarg, cvtarg):
    taudir = tau_dir(tau)
    targsdir = targs_dir(frttarg, cvtarg)
    return '{}_{}'.format(taudir, targsdir)


def noise_dir(noise):
    return 'std{:.3f}'.format(noise)


def noise_lab(noise):
    return '$\\sigma = {:.3f}$'.format(noise)
