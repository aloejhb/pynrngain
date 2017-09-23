import os
import sys
import imp
import argparse
import numpy as np
scriptdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(scriptdir, '..'))
from nrngain import jspar


parser = argparse.ArgumentParser()
parser.add_argument('cpfile', help='json file of cell parameter')
parser.add_argument('spkthr', type=float, help='json file of cell parameter')
parser.add_argument('ttime', type=float, help='total simulation time')
parser.add_argument('stimtyp', help='stimulation type')
parser.add_argument('spfile', help='json file of stimulation parameter')
parser.add_argument('outdir', help='output directory')
parser.add_argument('--moddir', help='path for model definition')
args = parser.parse_args()

if args.moddir:
    moddir = args.moddir
else:
    moddir = '.'
run = imp.load_source('run', os.path.join(moddir, 'run.py'))

stimpar = jspar.load(args.spfile)
cellpar = jspar.load(args.cpfile)
outdir = args.outdir

if not os.path.exists(outdir):
    raise OSError('No such directory: {}'.format(outdir))

spktimes, stimvec = run.simulation(cellpar, args.spkthr, args.ttime, args.stimtyp, stimpar, retstim=True)

runpar = dict(hpar=run.hpar,
              ttime=args.ttime,
              stimpar=stimpar,
              cellpar=cellpar,
              spkthr=args.spkthr)
rpfile = os.path.join(outdir, 'runpar.json')
jspar.save(rpfile, runpar)

with open(os.path.join(outdir, 'stimvec.npy'), 'w') as f:
    np.save(f, stimvec)

with open(os.path.join(outdir, 'spktimes.npy'), 'w') as f:
    np.save(f, spktimes)
