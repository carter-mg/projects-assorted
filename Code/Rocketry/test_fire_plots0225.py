# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 09:07:47 2025

@author: cmark
"""

import matplotlib.pyplot as plt
import pandas as pd
import os

os.chdir("C:/Users/cmark/Spyder/HybridRocketry/") # i use a conda distr, feel free to remove if your directory is all set.

# i am using a pandas dataframe.
data = pd.read_table("rundata0225.txt", delimiter= '\t')
data1 = pd.read_table("rundata.txt", delimiter= '\t')

# setting fonts and stuff.
plt.rcParams['font.family'] = 'Times New Roman'
scatter = plt.scatter(data['Time'], data['Thrust Zeroed'], s=.1, c = data['Thrust Zeroed'], cmap=  'viridis')

plt.colorbar(scatter)
plt.title("Thrust Against Time")
plt.xlabel("T (s)")
plt.ylabel("Force (lbf)")

plt.axvline(7.8, color='r', linestyle='--',linewidth= .4, label = 'Ignition')
plt.legend()

plt.show()
#%% ^ normalized
data1['adjusted time'] = data1['Time'] - 4.7
data['adjusted time'] = data['Time'] - 7

data1_time_adjust = data1[data1['Time'] >= 0].reset_index(drop = True)
data1_masked = data1_time_adjust.iloc[:len(data)].copy()

normalized1 = data['Thrust Zeroed'] / data1_masked['Thrust Zeroed']

plt.title("SF 2 Thrust Normal to Last")
plt.plot(data1_masked['adjusted time'], normalized1, color = 'r', linewidth =.5)
plt.xlabel("T (s)")
plt.ylabel("SF2 / SF1 Force (lbf)")
plt.xlim(2, 15)

plt.show()

#%% time and tank absolute
scatter2 = plt.scatter(data['Time'], data['Tank Absolute'], s=.1, c = data['Tank Absolute'], cmap=  'viridis')

plt.colorbar(scatter2)
plt.title("Tank Pressure Against Time")
plt.xlabel("T (s)")
plt.ylabel("Pressure (Psi)")

plt.axvline(7.8, color='r', linestyle='--',linewidth= .4, label = 'Ignition')
plt.legend()

plt.show()

#%% ^ normalized

normalized2 = data['Tank Absolute'] / data1_masked['Tank Absolute']

plt.title("SF 2 Tank Pressure Normal to Last")
plt.plot(data1_masked['adjusted time'], normalized2, color = 'r', linewidth =.5)
plt.xlabel("T (s)")
plt.ylabel("SF2 / SF1 Pressure (Psi)")
plt.xlim(0, 20)

plt.show()
#%% TC 1
scatter3 = plt.scatter(data['Time'], data['Thermo_1'], s=.1, c = data['Thermo_1'], cmap=  'viridis')

plt.colorbar(scatter3)
plt.title("Check Valve Thermal (1)")
plt.xlabel("T (s)")
plt.ylabel("Temperature (C)")

plt.axvline(7.8, color='r', linestyle='--',linewidth= .4, label = 'Ignition')
plt.legend()

plt.show()

#%% ^ normalized

normalized3 = data['Thermo_1'] / data1_masked['Thermo_1']

plt.title("SF 2 Check Valve Thermal (1) Normal to Last")
plt.plot(data1_masked['adjusted time'], normalized3, color = 'r', linewidth =.5)
plt.xlabel("T (s)")
plt.ylabel("SF2 /SF1 Temperature (C)")
plt.xlim(0, 20)

plt.show()
#%% TC 2
scatter4 = plt.scatter(data['Time'], data['Thermo_2'], s=.1, c = data['Thermo_2'], cmap=  'viridis')

plt.colorbar(scatter4)
plt.title("Tank Valve Thermal (2)")
plt.xlabel("T (s)")
plt.ylabel("Temperature (C)")

plt.axvline(7.8, color='r', linestyle='--',linewidth= .4, label = 'Ignition')
plt.legend()

plt.show()

#%% ^ normalized
normalized4 = data['Thermo_2'] / data1_masked['Thermo_2']

plt.title("SF 2 Tank Valve Thermal (2) Normal to Last")
plt.plot(data1_masked['adjusted time'], normalized4, color = 'r', linewidth =.5)
plt.xlabel("T (s)")
plt.ylabel("SF2 / SF1 Temperature (C)")
plt.xlim(0, 20)

plt.show()
#%% TC 3
scatter5 = plt.scatter(data['Time'], data['Thermo_3'], s=.1, c = data['Thermo_3'], cmap=  'viridis')

plt.colorbar(scatter5)
plt.title("Tank Side Thermal (4)")
plt.xlabel("T (s)")
plt.ylabel("SF2 / SF1 Temperature (C)")

plt.axvline(7.8, color='r', linestyle='--',linewidth= .4, label = 'Ignition')
plt.legend()

plt.show()

#%% TC 4
scatter6 = plt.scatter(data['Time'], data['Thermo_4'], s=.1, c = data['Thermo_4'], cmap=  'viridis')

plt.colorbar(scatter6)
plt.title("Run Valve Thermal (4)")
plt.xlabel("T (s)")
plt.ylabel("Temperature (C)")

plt.axvline(7.8, color='r', linestyle='--',linewidth= .4, label = 'Ignition')
plt.legend()

plt.show()

#%% TC 5
scatter7 = plt.scatter(data['Time'], data['Thermo_5'], s=.1, c = data['Thermo_5'], cmap=  'viridis')

plt.colorbar(scatter7)
plt.title("Injector Plate Thermal (5)")
plt.xlabel("T (s)")
plt.ylabel("Temperature (C)")

plt.axvline(7.8, color='r', linestyle='--',linewidth= .4, label = 'Ignition')
plt.legend()

plt.show()

#%% TC 6
scatter8 = plt.scatter(data['Time'], data['Thermo_6'], s=.1, c = data['Thermo_6'], cmap=  'viridis')

plt.colorbar(scatter8)
plt.title("Combustion Chamber Side Thermal (6)")
plt.xlabel("T (s)")
plt.ylabel("Temperature (C)")

plt.axvline(7.8, color='r', linestyle='--',linewidth= .4, label = 'Ignition')
plt.legend()

plt.show()

#%% TC 7
scatter9= plt.scatter(data['Time'], data['Thermo_7'], s=.1, c = data['Thermo_7'], cmap=  'viridis')

plt.colorbar(scatter9)
plt.title("Combustion Chamber Nozzle Thermal (7)")
plt.xlabel("T (s)")
plt.ylabel("Temperature (C)")

plt.axvline(7.8, color='r', linestyle='--',linewidth= .4, label = 'Ignition')
plt.legend()

plt.show()

#%% TC 8
scatter10 = plt.scatter(data['Time'], data['Thermo_8'], s=.1, c = data['Thermo_8'], cmap=  'viridis')

plt.colorbar(scatter10)
plt.title("Combustion Chamber Nozzle Thermal (8)")
plt.xlabel("T (s)")
plt.ylabel("Temperature (C)")

plt.axvline(7.8, color='r', linestyle='--',linewidth= .4, label = 'Ignition')
plt.legend()

plt.show()

#%% chamber TC combined

plt.plot(data['Time'], data['Thermo_6'], linewidth=.2, color='red', label='TC 6 (Chamber Side)')
plt.plot(data['Time'], data['Thermo_7'], linewidth=.2, color='blue', label='TC 7 (Chamber Nozzle)')
plt.plot(data['Time'], data['Thermo_8'], linewidth=.2, color='green', label='TC 8 (Chamber Nozzle)')

plt.axvline(7.8, color='black', linestyle='--',linewidth= .4, label = 'Ignition')

plt.title('Combustion Chamber Thermals')
plt.xlabel("T (s)")
plt.ylabel("Temperature (C)")
plt.legend()
plt.show()

#%% pressure transducers combined

plt.plot(data['Time'], data['Pressure Transducer 1'], linewidth=.2, color='red', label='Transducer 1 (Vent Valve)')
plt.plot(data['Time'], data['Pressure Transducer 2'], linewidth=.2, color='blue', label='Transducer 2 (Run Valve)')
plt.plot(data['Time'], data['Pressure Transducer 3'], linewidth=.2, color='green', label='Transducer 3 (Check Valve)')

plt.axvline(7.8, color='black', linestyle='--',linewidth= .4, label = 'Ignition')

plt.title('Pressure Transducers')
plt.xlabel("T (s)")
plt.ylabel("Pressure (Psi)")
plt.legend(fontsize = 'small')
plt.show()
