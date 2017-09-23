import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr


def hist_isi(spktimes):
    """Histogram of inter-spike intervals"""
    isi = np.diff(spktimes)
    return np.histogram(isi)


def srcr(spktimes, order):
    """Spearman rank correlation of inter-spike intervals"""
    isi = np.diff(spktimes)
    risi = np.roll(isi, order)
    res = spearmanr(isi[1:], risi[1:])
    return res


def cond_mean(spktimes, bins):
    """Conditional mean of inter-spike intervals"""
    isi = np.diff(spktimes)
    dig = np.digitize(isi, bins)
    cms = []
    for i in range(len(bins)-1):
        ind = np.where(dig[:-1] == i+1)[0]
        ind = map(lambda x: x+1, ind)
        cm = np.average(isi[ind])
        cms.append(cm)
    return cms


def plot_srcr(spktimes, norder, **kwargs):
    srcs = []
    for i in range(norder):
        src = srcr(spktimes, i+1)
        srcs.append(src[0])
    plt.plot(range(1,norder+1), srcs, '-o', **kwargs)


def plot_hist(spktimes, nbin, log=True, **kwargs):
    isi = np.diff(spktimes)
    # plt.hist(isi, nbin, **kwargs)
    y, binEdges = np.histogram(isi, bins=nbin)
    bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
    plt.semilogy(bincenters, y, '-o', **kwargs)


def plot_cond_mean(spktimes, bins=None, **kwargs):
    if bins is None:
        bins = np.arange(0, 400, 10)
    cms = cond_mean(spktimes, bins)
    plt.plot(bins[1:], cms, 'o', **kwargs)


if __name__ == '__main__':
    spktimes = np.load(sys.argv[2])

    if sys.argv[1] == 'spearmanr':
        norder = 20
        plot_srcr(spktimes, norder)
        plt.show()
    elif sys.argv[1] == 'hist':
        nbin = 100
        plot_hist(spktimes, nbin)
        plt.show()
    elif sys.argv[1] == 'cond_mean':
        plt.show()
