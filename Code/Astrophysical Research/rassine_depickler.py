import pickle
import matplotlib.pyplot as plt
import numpy as np
import os

os.chdir('/data/cartermg/code/rassine/Python_3.8/output/')
print(os.getcwd())
directory = input('Enter the directory of the .p files (c to cancel): ')

if directory.lower() != 'c':
    if directory == '':
         directory = os.getcwd()

    for file in os.listdir(directory):
            if file.lower().endswith('.p'):
                try:
                    file_path = os.path.join(directory, file)
                    with open(file_path, 'rb') as file:
                            data = pickle.load(file)

                    # get the data from the dictionary
                    out = data['output']
                    cubic = out['continuum_cubic']
                
                    title_name = file_path.split('/')[-1] + ' for ' + file_path.split('/')[-2]

                    wave = data['wave']
                    flux_used = data['flux_used']

                    # normalize the flux
                    plottable = np.divide(flux_used, cubic)

                    # plt settings

                    plt.rcParams['font.family'] = 'monospace'
                    plt.rcParams['text.usetex'] = False

                    # plotting
                    if wave[-1] > 10000:
                       
                        plt.figure(figsize=(28, 18))
                        plt.plot(wave, plottable, label='Flux')
                        
                        plt.title(f'Normalized Spectrum: {title_name}')
                        plt.xlabel('Wavelength (Angstrom)')
                        plt.ylabel('Normalized Flux')

                        plt.axhline(1, color = 'black', label = 'Normalized Flux = 1', linewidth = 0.5)

                        # for consistent dimensions of TSPEC. feel free to remove if wanted.
                    
                        plt.xlim(9800, 11000)
                        plt.ylim(0.8, 1.2)   

                        plt.axvline(10050, label='Paschen $\\delta$ 10050 A', color='red', linewidth=0.5)
                        plt.axvline(10940, label='Paschen $\\gamma$ 10940 A', color='green', linewidth=0.5)
                        plt.axvline(10835, label='He I 10835 A', color='blue', linewidth=0.5)

                        plt.legend(fontsize=8)

                        plt.show()
                        plt.close()

                    if wave[-1] < 9800:
                        # H alpha plot
                        plt.figure(figsize=(28, 18))
                        plt.plot(wave, plottable, label='Flux')
                        
                        plt.title(f'Normalized Spectrum: {title_name}')
                        plt.xlabel('Wavelength (Angstrom)')
                        plt.ylabel('Normalized Flux')

                        plt.axhline(1, color = 'black', label = 'Normalized Flux = 1', linewidth = 0.5)
                        plt.xlim(6500, 6600)
                        plt.ylim(0.2, 1.2)

                        plt.axvline(6563, label='H$\\alpha$, 6563 A', color='red', linewidth=0.5)        

                        plt.legend(fontsize=8)
                        plt.show()
                        plt.close()

                        # H beta plot
                        plt.figure(figsize=(28, 18))
                        plt.plot(wave, plottable, label='Flux')
                        
                        plt.title(f'Normalized Spectrum: {title_name}')
                        plt.xlabel('Wavelength (Angstrom)')
                        plt.ylabel('Normalized Flux')

                        plt.axhline(1, color = 'black', label = 'Normalized Flux = 1', linewidth = 0.5)
                        plt.xlim(4800, 4900)
                        plt.ylim(0.2, 1.2)

                        plt.axvline(4861, label='H$\\beta$, 4861 A', color='green', linewidth=0.5)

                        plt.legend(fontsize=8)
                        plt.show()
                        plt.close()

                except Exception as e:
                    print(f'Error processing file {file}: {e}')

                

if directory.lower() == 'c':
     print('Cancelled.')