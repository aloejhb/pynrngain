import os
import warnings
import numpy as np
import matplotlib.pyplot as plt
import pickle
import run
import neuron


def const_stim_rec(simfunc, amp, recnames, dur, delay):
    ttime = delay + dur
    stimpar = {'amp': amp, 'dur': dur, 'delay': delay}
    spktimes, recordings = simfunc(ttime, 'step', stimpar, None, recnames)
    return recordings


def plot_traj(v1, v2, st, ed, vnames):
    v1 = np.array(v1)
    v2 = np.array(v2)
    v1 = v1[st:ed]
    v2 = v2[st:ed]

    plt.plot(v1, v2)

    plt.xlabel(vnames[0])
    plt.ylabel(vnames[1])


def plot_const_stim_traj(simfunc, amp, varpr,
                         cst=300, ced=1900, dur=2000, delay=100):
    recs = const_stim_rec(simfunc, amp, varpr, dur, delay)
    plt.figure()
    plot_traj(recs[varpr[0]], recs[varpr[1]], cst, ced, varpr)


def plot_multi_traj(arr1, arr2, fir=0, num=100, rng=None,
                    vnames=None, units=None, label=None, **pltkwargs):
    if rng is None:
        rng = (0, arr1.shape[1])

    if fir > arr1.shape[0]:
        raise ValueError('First trajectory out of index')

    lst = fir+num
    if lst > arr1.shape[0]:
        warnings.warn('Total num trajectory exceeded')
        lst = arr1.shape[0]

    for i in range(fir, lst):
        v1 = arr1[i, rng[0]:rng[1]]
        v2 = arr2[i, rng[0]:rng[1]]
        if label and i == fir:
            plt.plot(v1, v2, label=label, **pltkwargs)
            continue
        plt.plot(v1, v2, **pltkwargs)

        if vnames:
            plt.xlabel(vnames[0])
            plt.ylabel(vnames[1])


def main():
    figmoddir = '../../figures/BSNaKReset'
    resmoddir = '../../results/BSNaKReset'
    # gnabar = 1e-3
    gnabar = 5e-3
    gnadir = 'gna%.0f' % (gnabar*1000)
    # gnadir = 'reset-20_gna%.0f' % (gnabar*1000)

    ppdir = os.path.join(figmoddir, gnadir, 'phase_plane')
    stmp_dir = os.path.join(resmoddir, gnadir, 'opt_stimpar')

    # h.celsius = 25.

    # soma = h.Section(name='soma')
    # vvec = np.linspace(-100, 50, 200)

    # nav = h.Nav_point(soma(0.5))
    # nav.gnabar = 1.
    # nav_vec = chnl.channel_property(nav, ['gna', 'minf', 'mtau'], vvec)
    # mvec = nav_vec['minf']
    # np.save(os.path.join(ppdir, 'vvec.npy'), vvec)
    # np.save(os.path.join(ppdir, 'mvec.npy'), mvec)

    
    # tau = 30.
    tau = 5.
    taudir = 'tau%.0f' % tau
    stmp_tau_dir = os.path.join(stmp_dir, taudir)
    if not os.path.exists(stmp_tau_dir):
        os.mkdir(stmp_tau_dir)

    ttime = 20000.
    targdir = 'frt5_cv1-0'
    gkscl_list = [0, 1, 3]
    gkbar_list = [gks * gnabar for gks in gkscl_list]
    fifo_trange = (-40., 0)
    # for gkbar in gkbar_list:
    #     ncellpar = {'gnabar': gnabar, 'gkbar': gkbar}

    #     gkdir = 'gk%.0f' % (gkbar*1e3)
    #     pardir = os.path.join(stmp_tau_dir, targdir, gkdir)
    #     spfile = os.path.join(pardir, 'stimpar.json')
    #     stimpar = parfunc.load_par(spfile)

    #     fifonames = ['time', 'v_soma', 'v_ais', 'icap_ais', 'nav_m', 'ina']
    #     if gkbar:
    #         fifonames.extend(['ik', 'kv_n'])

    #     outdir = os.path.join(ppdir, targdir, taudir, gkdir)
    #     if not os.path.exists(outdir):
    #         os.makedirs(outdir)

    #     # TODO define fifo_trange
    #     spktimes, pyfifos = run.simulation_OU(ttime, ncellpar, stimpar, fifonames=fifonames, fifo_trange=fifo_trange, outdir=outdir)
    #     print len(spktimes)
    
    # fi_dir = os.path.join(figmoddir, gnadir, 'fi_curve')
    # frt_targ = 5
    # for gkbar in gkbar_list:
    #     ncellpar = {'gnabar': gnabar, 'gkbar': gkbar}

    #     gkdir = 'gk%.0f' % (gkbar*1e3)

    #     outdir = os.path.join(ppdir, targdir, gkdir, 'cstim')
    #     if not os.path.exists(outdir):
    #         os.makedirs(outdir)

    #     gfidir = os.path.join(fi_dir, gkdir)
    #     threshs = parfunc.load_par(os.path.join(gfidir, 'threshs.json'))
    #     amp = threshs[str(frt_targ)][0]
   
    #     recnames = ['time', 'v_soma', 'v_ais', 'icap_ais', 'nav_m', 'ina']
    #     if gkbar:
    #         recnames.extend(['ik', 'kv_n'])

    #     rec_const_stim(ncellpar, amp, recnames, outdir)

    tau_li = [5, 30]
    # tau_li = [5]

    for tau in tau_li:
        taudir = 'tau%.0f' % tau
        # marker_list = ['o', '+', '>']
        color_li = ['#1f77b4', '#ff7f0e', '#2ca02c']
        leng = (1000, 1598)

        pair = ('v_ais', 'icap_ais')
        units = ('mV', 'nA')
        # pair = ('v_ais', 'nav_m')
        # units = ('mV', '')

        plt.figure(figsize=(8,7))
        vvec = np.load(os.path.join(ppdir, 'vvec.npy'))
        mvec = np.load(os.path.join(ppdir, 'mvec.npy'))

        figdir_base = os.path.join(figmoddir, gnadir, 'phase_plane')

        # plt.plot(vvec, mvec, label='$m_{\inf}$')
        for i, gkbar in enumerate(gkbar_list[:]):
            # plt.figure()
            gkdir = 'gk%.0f' % (gkbar*1e3)
            gklab = gkbar_label(gkbar)
            indir = os.path.join(ppdir, targdir, taudir, gkdir)
            plot_multi_traj(pair, indir, num=30, fir=15, leng=leng, units=units, label=gklab, color=color_li[i], alpha=0.2, ms=2)
            # marker=marker_list[i]

        plt.legend(loc=2, prop={'size': 12}, fancybox=True, framealpha=0.5)

        # plt.xlim((-50, -39.5))
        # plt.ylim((0.1, 0.55))
        figname = '%s-%s' % (pair[0], pair[1])

        # plt.xlim((-42, -39.9))
        # plt.ylim((0.385, 0.48))
        # figname = '%s-%s-zoom' % (pair[0], pair[1])
        figpath = os.path.join(figdir_base, targdir, taudir, figname+'.pdf')
        plt.savefig(figpath)
        plt.show()


        # cindir = os.path.join(indir, 'cstim')
        # dt = 0.025
        # cst = int(300/dt)
        # ced = int(1800/dt)
        # plot_traj(pair[0], pair[1], cindir, cst, ced)
        # figname = '%s-%s' % pair
        # plt.xlim((-50,-39))
        # plt.show()




if __name__ == '__main__':
    main()
