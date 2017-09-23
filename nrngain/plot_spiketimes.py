import sys
import numpy as np
import matplotlib.pyplot as plt

def plot_raster(spkt_list, **kwargs):
    for i, spkt in enumerate(spkt_list):
        plt.vlines(spkt, i, i+1, **kwargs)

def reshape_spkt(spkt, trial_time, ntrial):
    ttime = ntrial * trial_time
    spkt = spkt[spkt < ttime]
    spkt_list = []

    for i in range(ntrial):
        trspkt = spkt[(spkt > i*trial_time) & (spkt < (i+1)*trial_time)]
        trspkt = trspkt - i*trial_time
        spkt_list.append(trspkt)

    return spkt_list

    
if __name__ == '__main__':
    if len(sys.argv) == 2:
        figpath = None
    elif len(sys.argv) == 3:
        figpath= sys.argv[2]
    else:
        raise Exception('Usage: plot_spktimes.py spkt_file (figpath)')

    spktimes = np.load(sys.argv[1])
    spkt = spktimes[10:2000]
    spkt = spkt - spkt[0]
    trial_time = 2000
    ntrial = 20
    spkt_list = reshape_spkt(spkt, trial_time, ntrial)
    plot_raster(spkt_list)
    if figpath:
        plt.savefig(figpath)
    plt.show()
