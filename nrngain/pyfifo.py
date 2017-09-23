import os
import numpy as np
import pickle
import neuron

script_dir = os.path.dirname(__file__) + '/'

h = neuron.h
h.load_file('%s/hoc/FIFO.hoc' % script_dir)

# TODO check spkcount object before defining fifo_advance()
#    h('objref spkcount')
#    h.spkcount = spkcount


class PyFIFO:

    def __init__(self, name, rec, dur, dt):
        self.name = name
        self._rec = rec
        self._dur = dur
        self._veclen = int(float(self._dur)/dt)
        self._recptr = h.Pointer(rec)
        self.fifo = h.FIFO(self.name, self._recptr, self._veclen)
        h.fifolist.append(self.fifo)

    def get_matrix(self):
        mat = []
        for vec in self.fifo.veclist:
            mat.append(np.array(vec))
        mat = np.array(mat)
        return mat

    def get_svtimes(self):
        """Get time when FIFO is saved"""
        return np.array(self.fifo.svtimes)


def set_fifo_advance(spkcount, postfire_time, dt):
    h.load_file(1, '%s/hoc/fifo_advance.hoc' % script_dir)
    max_postfire_step = int(float(postfire_time)/dt) + 1

    h('objref fifospkc')
    h.fifospkc = spkcount

    h('max_postfire_step = %d' % max_postfire_step)
    h('''
      proc advance() {
        fadvance()
        fifo_advance(fifospkc)
      }
    ''')

# TODO check if fifo duration covers the spike duration
# TODO pass hoc name of spkcount as spkcount_hoc
# TODO check the robustness of spike detection with only spkcount.firing check


def create_fifos(fifodef, trange, spkcount):  # TODO validate trange
    h.fifolist = h.List()
    prefire_time = trange[0]
    postfire_time = trange[1]
    fifodur = postfire_time - prefire_time

    pyfifos = {}
    for name, rec in fifodef.iteritems():
        pyfifos[name] = PyFIFO(name, rec, fifodur, h.dt)

    set_fifo_advance(spkcount, postfire_time, h.dt)
    return pyfifos


def pyfifos_to_dict(pyfifos):
    fifos = {k: v.get_matrix() for k, v in pyfifos.items()}
    return fifos


def save_fifos(fifos, outdir, separate=False):
    print 'Saving FIFO recordings'

    if separate:
        fifodir = os.path.join(outdir, 'fifo')
        if not os.path.exists(fifodir):
            os.mkdir(fifodir)

        for k, v in fifos.items():
            fmat = os.path.join(fifodir, '{}.npy'.format(k))
            with open(fmat, 'w') as f:
                np.save(f, v)
    else:
        with open(os.path.join(outdir, 'fifos.p'), 'w') as f:
            pickle.dump(fifos, f)
