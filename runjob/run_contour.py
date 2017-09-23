import os
import argparse
import sys
import imp
import numpy as np
import logging
scriptdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(scriptdir, '..'))
from nrngain import jspar, contour

parser = argparse.ArgumentParser()
parser.add_argument('outdir', help='output directory')
parser.add_argument('cpfile', help='json file of cell parameter')
parser.add_argument('spkthr', type=float, help='json file of cell parameter')
parser.add_argument('fxvfile', help='numpy file of fixed value vector')
parser.add_argument('bracket', type=float, nargs=2, help='search bracket for x')
parser.add_argument('xname', help='parameter name for optimization')
parser.add_argument('tau', type=float, help='time constant of OU process')
parser.add_argument('statname', help='spike statistic variable for contour')
parser.add_argument('targ', type=float, help='value of statistic variable for contour')
parser.add_argument('ttime', type=float, help='total simulation time')
parser.add_argument('--rseed', type=int, default=3,  help='random number seed for OU')
parser.add_argument('--moddir', help='path for model definition')
args = parser.parse_args()

if args.moddir:
    moddir = args.moddir
else:
    moddir = '.'
run = imp.load_source('run', os.path.join(moddir, 'run.py'))

outdir = args.outdir
if not os.path.exists(outdir):
    raise OSError('No such output directory: %s' % outdir)
cellpar = jspar.load(args.cpfile)
fxvec = np.load(args.fxvfile)

logfile = os.path.join(outdir, 'contour.log')
logging.basicConfig(filename=logfile, level=logging.INFO)

simfunc = run.cellpar_wrapper(run.simulation, cellpar, args.spkthr)
targfunc = contour.targfunc_wrapper(simfunc, args.xname, args.tau, args.statname, args.targ, args.ttime, rseed=args.rseed)
xvec = contour.get_contour(targfunc, fxvec, args.bracket)

logging.info(str(xvec))
np.save(os.path.join(args.outdir, 'xvec.npy'), xvec)

jspar.save(os.path.join(args.outdir, 'ctpar.json'), vars(args))
