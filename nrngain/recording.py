import os
import numpy as np
import matplotlib.pyplot as plt
import neuron


def create_recordings(record_dict):
    """
    Create recording vectors for NEURON module simulation
    input:
        record_dict: dictionary with key as name of recording,
                     value as recording object.
    output:
        recordings: dictionary with key as name of recording,
                    value as NEURON recording Vector object
    """
    recordings = {}
    for name, recref in record_dict.items():
        recordings[name] = neuron.h.Vector()
        recordings[name].record(recref)

    return recordings


def recordings_to_dict(recordings):
    recs = {k: np.array(v) for k, v in recordings.items()}
    return recs


def save_recordings(recordings, outdir):
    print 'Saving recordings'
    recdir = os.path.join(outdir, 'recordings')
    for k, v in recordings.iteritems():
        fpath = os.path.join(recdir, '%s.npy' % k)
        np.save(fpath, np.array(v))


def plot_recordings(recordings, varnames=None, tvec=None):

    if tvec is None:
        if 'time' in recordings:
            tvec = recordings['time']
        else:
            raise Exception('No tvec provided and no time vector in recordings!')

    if varnames is None:
        varnames = [k for k in recordings.keys() if k != 'time']

    for var in varnames:
        varvec = recordings[var]
        plt.figure()
        plt.plot(tvec, varvec)
        plt.xlabel('time (ms)')
        plt.ylabel(var)
