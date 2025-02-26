# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 12:38:03 2024

@author: cmark
"""
import numpy as np 
import matplotlib.pyplot as plt

## nitrous amounts possible for different conditions. 

## constants

R = 8.314
V = 1.5 #m^3

T_range = np.linspace(100, 400, 100) #kelvin
P_range = np.linspace(1e5, 5e6, 100) #pascal

P, T = np.meshgrid(P_range, T_range)

n = (P * V) / (R * T) #ideal gas law

## adding vaporization point for nitrous

vap_plane = 6.8e5  #pascal
n_plane = (vap_plane * V) / (R * T_range[:, np.newaxis]) 

fig = plt.figure(figsize = (10,7))
ax = fig.add_subplot(111, projection = '3d')

surface = ax.plot_surface(T,P/1e5, n, cmap='viridis', edgecolor = 'k', alpha = 0.9)

## including the vaporization plane
T_plane, n_plane_grid = np.meshgrid(T_range, n_plane)
ax.plot_surface(
    T_plane, np.full_like(T_plane, vap_plane / 1e5), n_plane_grid, color='red', alpha=0.9
)

ax.set_title('n against T and P')
ax.set_xlabel('temp (K)')
ax.set_ylabel('pressure (bar)')
ax.set_zlabel('moles (n)')
ax.view_init(30,210)

## color function

cbar = fig.colorbar(surface, ax = ax, shrink = .5, aspect = 10)
cbar.set_label('moles (n)', fontsize = 11)

plt.show