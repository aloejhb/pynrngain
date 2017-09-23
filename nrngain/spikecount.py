import os
import sys
import numpy as np
import matplotlib.pyplot as plt

import neuron
h = neuron.h

def create_spkcount(section, loc, spk_thresh):
    # try:
    #    section_name = section.hname()
    # except:
    #     raise Exception('Given object is not a section with name!')

    # Use hoc string to define spkcount object,
    # as spkcount is used in h.advance() function for FIFO memory.
    # See ./pyfifo.py
    # h('%s spkcount = new APCount()' % section_name)
    # h.spkcount.loc(loc)

    # spkcount = h.spkcount

    spkcount = h.APCount(loc, sec=section)
    spkcount.thresh = spk_thresh

    spktimes = h.Vector()
    spkcount.record(spktimes)

    return spkcount, spktimes
