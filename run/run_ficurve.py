import os
import sys
import imp
import argparse
import numpy as np
scriptdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(scriptdir, '..'))
from nrngain import ficurve, jspar


parser = argparse.ArgumentParser()
parser.add_argument('ctvfile', help='numpy file of current value vector')
parser.add_argument('cpfile', help='json file of cell parameter')
parser.add_argument('spkthr', type=float, help='voltage thresh for spike detection')
parser.add_argument('outdir', help='output directory')
parser.add_argument('--moddir', help='path for model definition')
parser.add_argument('--noise', type=float, help='0: no noise, non-0: standard deviation of OU process')
parser.add_argument('--tau', type=float, help='tau for OU process')
args = parser.parse_args()


if args.moddir:
    moddir = args.moddir
else:
    moddir = '.'
run = imp.load_source('run', os.path.join(moddir, 'run.py'))

curtvec = np.load(args.ctvfile)
cellpar = jspar.load(args.cpfile)
outdir = args.outdir

if not os.path.exists(outdir):
    raise Exception('No such directory: %s' % outdir)

simfunc = run.cellpar_wrapper(run.simulation, cellpar, args.spkthr)
frtvec = ficurve.get_frtvec(simfunc, curtvec, noise=args.noise, tau=args.tau)
np.save(os.path.join(outdir, 'frtvec.npy'), frtvec)

jspar.save(os.path.join(outdir, 'fipar.json'), vars(args))
