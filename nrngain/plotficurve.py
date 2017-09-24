import os
import numpy as np
import matplotlib.pyplot as plt


def plot_ficurve(indir, marker='o-', **kwargs):
    curtvec = np.load(os.path.join(indir, 'curtvec.npy'))
    frtvec = np.load(os.path.join(indir, 'frtvec.npy'))
    plt.plot(curtvec, frtvec, marker, **kwargs)
