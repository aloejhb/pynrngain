import os
import sys
import numpy as np
from subprocess import call
sys.path.append('../../')
from nrngain import jspar

rjpath = os.path.realpath(__file__)


def submit_to_cluster(qname, jobname, script, args):
    args = [str(arg) for arg in args]
    command = ['qsub', '-q', qname, '-N', jobname, 'submit.sh', script] + args
    call(command)


def run_ficurve(qname, curtvec, cellpar, spkthr, outdir, noise=0, tau=0):
    cpfile = os.path.join(outdir, 'cellpar.json')
    jspar.save(cpfile, cellpar)

    ctvfile = os.path.join(outdir, 'curtvec.npy')
    np.save(ctvfile, curtvec)

    args = [ctvfile, cpfile, spkthr, outdir, '--noise', noise, '--tau', tau]
    scpath = os.path.join(rjpath, 'run_ficurve.py')
    submit_to_cluster(qname, 'ficurve', scpath, args)


def run_optstimpar(qname, outdir, cellpar, spkthr, x0, *optmargs):
    spkthrfile = os.path.join(outdir, 'spkthr.json')
    jspar.save(spkthrfile, spkthr)
    cpfile = os.path.join(outdir, 'cellpar.json')
    jspar.save(cpfile, cellpar)

    args = [outdir, cpfile, spkthr, x0[0], x0[1]]
    args.extend(optmargs)
    scpath = os.path.join(rjpath, 'run_optstimpar.py')
    submit_to_cluster(qname, 'optstm', scpath, args)


def run_simulation(qname, ttime, outdir, pardir):
    spkthrfile = os.path.join(pardir, 'spkthr.json')
    cpfile = os.path.join(pardir, 'cellpar.json')
    spfile = os.path.join(pardir, 'stimpar.json')

    if (not (os.path.exists(pardir)
             and os.path.isfile(cpfile)
             and os.path.isfile(spfile)
             and os.path.isfile(spkthrfile))):
        raise Exception('Please run run_optstimpar() before run_simulation()! pardir {}'.format(pardir))

    if not os.path.exists(outdir):
        raise OSError('No such directory: {}'.format(outdir))

    spkthr = jspar.load(spkthrfile)
    stimtyp = 'OU'
    args = [cpfile, spkthr, ttime, stimtyp, spfile, outdir]
    scpath = os.path.join(rjpath, 'run_simulation.py')
    submit_to_cluster(qname, 'sim', scpath, args)


def run_sta(qname, indir):
    scpath = os.path.join(rjpath, 'run_sta.py')
    submit_to_cluster(qname, 'sta', scpath, [indir])
