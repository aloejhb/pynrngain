import os
import sys
import argparse
import numpy as np
scriptdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(scriptdir, '..'))
from nrngain import jspar, spktrigavrg

parser = argparse.ArgumentParser()
parser.add_argument('indir', help='input directory contains spktimes, stimvec, runpar')
parser.add_argument('--maxtau', help='time range of stimulus before and after spike (ms)')
args = parser.parse_args()

indir = args.indir
if not os.path.exists(indir):
    raise OSError('No such directory: {}'.format(indir))

spktimes = np.load(os.path.join(indir, 'spktimes.npy'))
stimvec = np.load(os.path.join(indir, 'stimvec.npy'))
runpar = jspar.load(os.path.join(indir, 'runpar.json'))

if args.maxtau:
    maxtau = args.maxtau
else:
    maxtau = 500.

dt = runpar['hpar']['dt']
stim_mean = runpar['stimpar']['mean']

sta = spktrigavrg.get_sta(stimvec, spktimes, maxtau, dt, stim_mean)
np.save(os.path.join(indir, 'sta.npy'), sta)
