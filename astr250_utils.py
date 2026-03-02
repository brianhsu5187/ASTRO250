#!/usr/bin/env python
# coding: utf-8
# %%

# %%


from specutils import Spectrum1D
from matplotlib import pyplot as plt
import numpy as np
from astroML.datasets import fetch_sdss_filter, fetch_vega_spectrum


# %%


def plot_gal_spectra():
    ## hide this into a function
    spiral = Spectrum1D.read('/Users/brianhsu/Downloads/sed/ngc6221.fits')
    # spiral.flux[spiral.flux.value<0] = np.nan
    elliptical = Spectrum1D.read('/Users/brianhsu/Downloads/sed/ngc7196.fits')
    # elliptical.flux[elliptical.flux.value<0] = np.nan

    fig, ax = plt.subplots(2,1, figsize=(10,5), sharex=True)
    plt.subplots_adjust(hspace=0.2)

    ax[0].plot(elliptical.spectral_axis, elliptical.flux.value, color='k', lw=1)
    ax[1].plot(spiral.spectral_axis, spiral.flux.value, color='k', lw=1)

    for a in ax:
    #     a.set_yscale('log')
        a.set_ylabel('Flux Density', fontsize=12)
        a.minorticks_on()
        a.set_xlim(3000,10000)
    ax[1].set_xlabel('Wavelength (${\\rm \\AA}$)', fontsize=12)
    ax[0].set_title('No Star Formation')
    ax[1].set_title('Active Star Formation')
    plt.show()


# %%
def plot_gal_spectra_w_filters():
    ## hide this into a function
    spiral = Spectrum1D.read('/Users/brianhsu/Downloads/sed/ngc6221.fits')
    spiral.flux[spiral.flux.value<0] = np.nan
    elliptical = Spectrum1D.read('/Users/brianhsu/Downloads/sed/ngc7196.fits')
    elliptical.flux[elliptical.flux.value<0] = np.nan

    fig, ax = plt.subplots(2,1, figsize=(10,5), sharex=True)
    plt.subplots_adjust(hspace=0.3)

    ax[0].plot(elliptical.spectral_axis, elliptical.flux.value/np.nanmax(elliptical.flux.value), color='k', lw=1)
    ax[1].plot(spiral.spectral_axis, spiral.flux.value/np.nanmax(spiral.flux.value), color='k', lw=1)

    text_kwargs = dict(ha='center', va='center', alpha=1, fontsize=18)

    for f, c, loc in zip('ugriz', 'bgrmk', [3551, 4686, 6166, 7480, 8932]):
        data = fetch_sdss_filter(f)
        for a in ax:
            a.fill(data[0], data[1]/data[1].max(), ec=c, fc=c, alpha=0.2)
        ax[0].text(loc, 0.1, f, color=c, **text_kwargs)
        ax[1].text(loc, 0.6, f, color=c, **text_kwargs)

    for a in ax:
        a.set_xlim(3000, 10000)
    #     a.set_yscale('log')
        a.set_ylabel('Flux Density', fontsize=12)
        a.minorticks_on()
        a.set_yticklabels([])
    ax[1].set_xlabel('Wavelength (${\\rm \\AA}$)', fontsize=12)
    ax[0].set_title('No Star Formation',fontsize=16)
    ax[1].set_title('Active Star Formation',fontsize=16)
    plt.show()
