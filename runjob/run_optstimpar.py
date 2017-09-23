import os
import argparse
import sys
import imp
import logging
scriptdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(scriptdir, '..'))
from nrngain import jspar, optstimpar


parser = argparse.ArgumentParser()
parser.add_argument('outdir', help='output directory')
parser.add_argument('cpfile', help='json file of cell parameter')
parser.add_argument('spkthr', type=float, help='json file of cell parameter')
parser.add_argument('mean0', type=float, help='initial guess of mean')
parser.add_argument('std0', type=float, help='initial guess of std')
parser.add_argument('tau', type=float, help='tau of OU process')
parser.add_argument('ttime', type=float, help='total simulation time for one evaluation')

parser.add_argument('frttarg', type=float, help='target firing rate')
parser.add_argument('cvtarg', type=float, help='target cv')
parser.add_argument('--moddir', help='path for model definition')

args = parser.parse_args()

if args.moddir:
    moddir = args.moddir
else:
    moddir = '.'
run = imp.load_source('run', os.path.join(moddir, 'run.py'))

outdir = args.outdir
if not os.path.exists(outdir):
    raise Exception('No such output directory: %s' % outdir)
cellpar = jspar.load(args.cpfile)
x0 = (args.mean0, args.std0)

logfile = os.path.join(outdir, 'optstimpar.log')
logging.basicConfig(filename=logfile, level=logging.INFO)


simfunc = run.cellpar_wrapper(run.simulation, cellpar, args.spkthr)
ostimpar, res = optstimpar.optstimpar(simfunc, x0, args.tau, args.ttime, args.frttarg, args.cvtarg)

spfile = os.path.join(outdir, 'stimpar.json')
jspar.save(spfile, ostimpar)
