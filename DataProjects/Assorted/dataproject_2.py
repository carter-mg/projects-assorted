# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 15:05:27 2025

@author: cmark
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.optimize import curve_fit

os.chdir("C:/Users/cmark/Spyder/PHSCS 428/")

HD1data = pd.read_table("HD28745.txt", delim_whitespace = 'true')

HD2data = pd.read_table("HD62542.txt", delim_whitespace= 'true')

BVdata = pd.read_table("B57V.txt", delim_whitespace= 'true')

# setting fonts and stuff.
plt.rcParams['font.family'] = 'Times New Roman'
#scatter2 = plt.scatter(HD2data['#Wavelength(Ang.A)'], HD2data['F_lambda(10^-12ergs/s/cm^2/A)'], s=.1, c = HD2data['F_lambda(10^-12ergs/s/cm^2/A)'], cmap=  'viridis')

HD1_clean = HD1data[(HD1data['#Wavelength(Ang.A)'] >= 1200) & (HD1data['#Wavelength(Ang.A)'] <= 1800) ]
HD2_clean = HD2data[(HD1data['#Wavelength(Ang.A)'] >= 1200) & (HD2data['#Wavelength(Ang.A)'] <= 1800) ]
template_clean = BVdata[(BVdata['#Wavelength(Ang.A)'] >= 1200) & (BVdata['#Wavelength(Ang.A)'] <= 1800) ]

HD1max_clean = HD1_clean['F_lambda(10^-12ergs/s/cm^2/A)'].max()
HD2max_clean = HD2_clean['F_lambda(10^-12ergs/s/cm^2/A)'].max()
BVmax_clean1 = 2.4* template_clean['F_lambda(10^-12ergs/s/cm^2/A)'].max()
BVmax_clean2 = .8 * template_clean['F_lambda(10^-12ergs/s/cm^2/A)'].max()


# printing 

print(f'HD 28475 Max: {HD1max_clean}')
print(f'HD 62542 Max: {HD2max_clean}')
print(f'Template 1 Max (Scaled): {BVmax_clean1}')
print(f'Template 2 Max (Scaled): {BVmax_clean2}')



ratio_actual1 = HD1max_clean / BVmax_clean1
ratio_actual2 = HD2max_clean / BVmax_clean2

print(f'HD 28475 Actual Flux Ratio: {ratio_actual1}')
print(f'HD 62542 Actual Flux Ratio: {ratio_actual2}')

#%%
plt.figure()

plt.scatter(HD1data['#Wavelength(Ang.A)'], HD1data['F_lambda(10^-12ergs/s/cm^2/A)'], s=.1, c = HD1data['F_lambda(10^-12ergs/s/cm^2/A)'], cmap=  'viridis')
plt.plot(BVdata['#Wavelength(Ang.A)'], 2.4*BVdata['F_lambda(10^-12ergs/s/cm^2/A)'], color='r')
plt.title("HD28475")
plt.xlabel("Wavelength (A)")
plt.ylabel("F$_\lambda (10^{-12}ergs/s/cm^2/A)$")
plt.show()


#%%
plt.figure()
plt.scatter(HD2data['#Wavelength(Ang.A)'], HD2data['F_lambda(10^-12ergs/s/cm^2/A)'], s=.1, c = HD2data['F_lambda(10^-12ergs/s/cm^2/A)'], cmap=  'viridis')
plt.plot(BVdata['#Wavelength(Ang.A)'], .8*BVdata['F_lambda(10^-12ergs/s/cm^2/A)'], color='r')
plt.title("HD62542")
plt.xlabel("Wavelength (A)")
plt.ylabel("F$_\lambda (10^{-12}ergs/s/cm^2/A)$")
plt.show()

#%%

HD1conv = HD1data.copy()
HD1conv['#Wavelength(Ang.A)'] = HD1conv['#Wavelength(Ang.A)'] * 1e-4
x = 1 / HD1conv['#Wavelength(Ang.A)']

Alambda1 = -2.5 * np.log10(HD1data['F_lambda(10^-12ergs/s/cm^2/A)'] / BVdata['F_lambda(10^-12ergs/s/cm^2/A)'])

# slope finding stuff
def line_func(x, a, b):
    return a*x + b

range1 = (1.5, 3)
range2 = (5, 8)
mask1 = (x >= range1[0]) & (x <= range1[1])
mask2 = (x >= range2[0]) & (x <= range2[1])

x_region1 = x[mask1]
Alambda1_region1 = Alambda1[mask1]

x_region2 = x[mask2]
Alambda1_region2 = Alambda1[mask2]

popt1, pcov1 = curve_fit(line_func, x_region1, Alambda1_region1)
popt2, pcov2 = curve_fit(line_func, x_region2, Alambda1_region2)

print(f"Fitted parameters: a = {popt1[0]}, b = {popt1[1]}")
print(f"Fitted parameters: a = {popt2[0]}, b = {popt2[1]}")

plt.figure()
plt.title('HD 28475 A$_{\lambda}$ with Optimized Slopes')
plt.xlabel('$\mu^{-1}$')
plt.ylabel("$A_\lambda$")
plt.plot(x_region1, line_func(x_region1, *popt1), 'r-', label='Fitted Line Region 1')
plt.plot(x_region2, line_func(x_region2, *popt2), 'g-', label='Fitted Line Region 2')
plt.plot(x, Alambda1)

#%%

HD2conv = HD2data.copy()
HD2conv['#Wavelength(Ang.A)'] = HD2conv['#Wavelength(Ang.A)'] * 1e-4
x = 1 / HD2conv['#Wavelength(Ang.A)']

Alambda2 = -2.5 * np.log10(HD2data['F_lambda(10^-12ergs/s/cm^2/A)'] / BVdata['F_lambda(10^-12ergs/s/cm^2/A)'])

# slope finding stuff
def line_func(x, a, b):
    return a*x + b

range1 = (1.5, 3)
range2 = (4.0, 8)
mask1 = (x >= range1[0]) & (x <= range1[1])
mask2 = (x >= range2[0]) & (x <= range2[1])

x_region1 = x[mask1]
Alambda2_region1 = Alambda2[mask1]

x_region2 = x[mask2]
Alambda2_region2 = Alambda2[mask2]

popt1, pcov1 = curve_fit(line_func, x_region1, Alambda2_region1)
popt2, pcov2 = curve_fit(line_func, x_region2, Alambda2_region2)

print(f"Fitted parameters: a = {popt1[0]}, b = {popt1[1]}")
print(f"Fitted parameters: a = {popt2[0]}, b = {popt2[1]}")

plt.figure()
plt.title('HD 62542 A$_{\lambda}$ with Optimized Slopes')
plt.xlabel('$\mu^{-1}$')
plt.ylabel("$A_\lambda$")
plt.plot(x_region1, line_func(x_region1, *popt1), 'r-', label='Fitted Line Region 1')
plt.plot(x_region2, line_func(x_region2, *popt2), 'g-', label='Fitted Line Region 2')
plt.plot(x, Alambda2)