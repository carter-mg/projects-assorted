import os
import numpy as np

from astropy.io import fits
from astropy import units as u

# simple script that writes .csv files for processing from .fits filesk, expecting standard formatting and headers. 

entry = 'UT250326' # enter target directory here
base = '/data/cartermg/V927Her/irspectra/' # base directory for the script

directory = os.path.join(base,entry)

try: 
    for file in os.listdir(directory):
        if file.lower().endswith(('.fit', '.fits')):
            file_path = os.path.join(directory, file)
            with fits.open(file_path) as hdul:
                data = hdul[0].data
                header = hdul[0].header

                flux = data[1]
                wavelength = data[0]

                base_name = os.path.splitext(file)[0]
                output_csv = os.path.join(directory, f'{base_name}.spectrum.csv')

            mask = (wavelength > 0.974) & (wavelength < 1.110)

            wl = wavelength[mask]
            f = flux[mask]

            # f /= np.median(f) # comment this out if your flux values are much greater than 1e-13 erg/s/cm^2/A
            wl = np.multiply(wl, 10000) # to angstrom

            col = np.column_stack((wl, f))


            np.savetxt(output_csv, col, delimiter=',', header='wave,flux', comments='')
            print(f'I successfully wrote the file {base_name}.spectrum.csv in {directory}.')
            print(f'Wavelength converted to Angstrom for RASSINE Processing.\n')

except FileNotFoundError as e:
    print(f'Invalid directory or file name: {e}')

