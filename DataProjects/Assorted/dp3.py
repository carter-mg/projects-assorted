# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 11:43:44 2025

@author: cmark
"""

## data import

import pandas as pd
import os 
import matplotlib.pyplot as plt
import numpy as np

os.chdir("C:/Users/cmark/Spyder/PHSCS 428")

data = pd.read_csv('Pleiades-result.csv')

#%% plotting
plt.rcParams['font.family'] = 'Times New Roman'

plt.figure()
plt.scatter(data['phot_bp_mean_mag'] - data['phot_rp_mean_mag'], data['phot_g_mean_mag'], s=.2, color='black')
plt.xlabel("$G_{BP} - G_{RP}$")
plt.ylabel("$G$")
plt.show()

#%% startng cuts

## from NASA, distance is 445 ly = 136.43 pc, which is about 7.4 arcsec

plt.hist(data['parallax'], bins=25, range= (-5, 8), edgecolor='black')
plt.title('$\pi$ Histogram')
plt.xlabel('$\pi$ (arcsec)')
plt.ylabel('Occurence')

data_parallax = data[(data['parallax'] >= 6) & (data['parallax'] <= 8)]

#%% RA Proper Motion

plt.hist(data_parallax['ra_pmra_corr'], bins =25, edgecolor='black')
plt.title('RA $\mu$ Histogram')
plt.xlabel('$\mu_{RA}$ ()')
plt.ylabel('Occurence')

data_rapm= data_parallax[(data_parallax['ra_pmra_corr']>=-0.5) & (data_parallax['ra_pmra_corr'] <=.3)]
#%% Dec Proper Motion

plt.hist(data_parallax['dec_pmdec_corr'], bins =25, edgecolor='black')
plt.title('Dec $\mu$ Histogram')
plt.xlabel('()')
plt.ylabel('Occurence')

data_decpm = data_rapm[(data_rapm['dec_pmdec_corr'] >= -0.1) & (data_rapm['dec_pmdec_corr'] <= 0.9)]
#%% Position

plt.figure()
plt.hist(data_parallax['ra'], bins =25, edgecolor='black')
plt.title('RA Position Histogram')
plt.xlabel(' ()')
plt.ylabel('Occurence')
plt.show() 

plt.figure()
plt.hist(data_parallax['dec'], bins =25, edgecolor='black')
plt.title('Dec Histogram')
plt.xlabel('()')
plt.ylabel('Occurence')
plt.show()

data_pra = data_decpm[(data_decpm['ra'] >= 54.5) & (data_decpm['ra'] <= 58.5)]
data_pdec = data_pra[(data_pra['dec'] >= 22) & (data_pra['dec'] <= 27)]

#%% final CMD

datafinal = data_pdec

plt.figure()
plt.title('Color Magnitude Diagram Final')
plt.scatter(datafinal['phot_bp_mean_mag'] - datafinal['phot_rp_mean_mag'], datafinal['phot_g_mean_mag'], s=.2, color='black')
plt.xlabel("$G_{BP} - G_{RP}$")
plt.ylabel("$G$")
plt.show()

plt.figure()
plt.title('Color Magnitude Diagram Combined')
plt.scatter(data['phot_bp_mean_mag'] - data['phot_rp_mean_mag'], data['phot_g_mean_mag'], s=.2, color='black')
plt.scatter(datafinal['phot_bp_mean_mag'] - datafinal['phot_rp_mean_mag'], datafinal['phot_g_mean_mag'], s=.2, color='red')
plt.xlabel("$G_{BP} - G_{RP}$")
plt.ylabel("$G$")
plt.show()


#%% vector plot

plt.figure()
plt.title('VPD')
plt.scatter(data['ra_pmra_corr']*np.cos(data['dec_pmdec_corr']), data['dec_pmdec_corr'], s=.04)
plt.xlabel('RA')
plt.ylabel('Dec')
plt.show()

plt.figure()
plt.title('VPD Final')
plt.scatter(datafinal['ra_pmra_corr']*np.cos(datafinal['dec_pmdec_corr']), datafinal['dec_pmdec_corr'], s=.8)
plt.xlabel('RA')
plt.ylabel('Dec')
plt.show()

plt.figure()
plt.title('VPD Combined')
plt.scatter(data['ra_pmra_corr']*np.cos(data['dec_pmdec_corr']), data['dec_pmdec_corr'], s=.04)
plt.scatter(datafinal['ra_pmra_corr']*np.cos(datafinal['dec_pmdec_corr']), datafinal['dec_pmdec_corr'], s=.8, color='red')
plt.xlabel('RA')
plt.ylabel('Dec')
plt.show()

#%%

average = datafinal['parallax'].mean() /1000
print(f"Average value: {average}")

distance = 1/average
print(f"Calculated Distance: {distance}")