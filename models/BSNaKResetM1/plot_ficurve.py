import os
import sys
import matplotlib.pyplot as plt
import labeldir
sys.path.append('../../')
from nrngain import plotficurve


def plot_ficurves(gkbarli, indir, marker='o-', labapd='', colorli=None, **kwargs):
    for i, gkbar in enumerate(gkbarli):
        gkdir = labeldir.gkbar_dir(gkbar)
        lab = labeldir.gkbar_lab(gkbar)
        if labapd:
            lab = lab + labapd
        subdir = os.path.join(indir, gkdir)
        if colorli:
            color = colorli[i]
            kwargs['color'] = color

        plotficurve.plot_ficurve(subdir, marker, label=lab, **kwargs)


def plot_noise_ficurves(noise, gkbarli, indir, colorli, nscolorli):
    nsdir = os.path.join(indir, labeldir.noise_dir(noise))
    znsdir = os.path.join(indir, labeldir.noise_dir(0))

    plot_varygk_ficurve(gkbarli, znsdir, 'o-', colorli=colorli, ms=2.)
    plot_varygk_ficurve(gkbarli, nsdir, '--', labapd=' w/ noise', colorli=nscolorli, linewidth=2., alpha=0.4)
    plt.xlabel('Mean of input current (nA)')
    plt.xlim((0, 0.15))
    plt.ylabel('Firing rate (Hz)')
    plt.ylim((0, 90))
    plt.legend(loc=2, fancybox=True, framealpha=0.5)
    plt.minorticks_on()
    plt.savefig(os.path.join(indir, 'fi_curve_noise.pdf'))
    plt.show()


if __name__ == '__main__':
    figdir = '../../figures/BSNaKResetNew/'
    fidir = os.path.join(figdir, 'fi_curve')
    gkbarli = [0, 5e-3, 15e-3]
    noise = 0.02
    colorli = ['#1f77b4', '#ff7f0e', '#2ca02c']
    nscolorli = ['darkblue', 'chocolate', 'darkgreen']
    plot_noise_ficurves(noise, gkbarli, fidir, colorli, nscolorli)

