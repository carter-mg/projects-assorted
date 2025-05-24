"""
    A script for generating plots of optical spectra (expects standard .fits heading and formatting).
    Includes kgullikson88's readmultispec() function-- GitHub: https://github.com/kgullikson88/General/blob/master/readmultispec.py

    Mainly for data processing and visualization. Produces .csv's for processing in Michael Cretignier's RASSINE code for spectral normalization.

    Execute from the terminal. 

    -----------------
    BASIC RULES
    -----------------
    1. In cmdl, python optical_viewer.py
    2. CSV file production first. Will create a directory full of .csv files with flux and wavelength values for each .fit/.fits file in the directory.
    3. Plot generator second. Will produce plots, then ask if you want to specify ranges for saving the figure. Feel free to save manually as well.
    
    All of this makes normalization and fitting much easier in RASSINE.


"""


import matplotlib.pyplot as plt
import numpy as np
import os
import warnings
# import pickle

from astropy.io import fits
from astropy import units as u
# from astropy.wcs import WCS

from readmultispec import readmultispec

def plot_spectrum(wavelength, flux, title, xlims = None, ylims = None, save_path = None):
    plt.rcParams['font.family'] = 'monospace'
    plt.rcParams['text.usetex'] = False

    plt.figure(figsize= (10,7))
    plt.plot(wavelength, flux, linewidth = 0.4)
    if xlims: plt.xlim(xlims[0], xlims[1])
    if ylims: plt.ylim(ylims[0], ylims[1])
    plt.xlabel('Angstrom')
    plt.ylabel('Erg/s/cm$^2$/A ??')
    plt.axvline(6563, label = 'H$\\alpha$, 6563 A', color = 'red', linewidth = 0.5)
    plt.axvline(4861, label = 'H$\\beta$, 4861 A', color = 'green', linewidth = 0.5)
    plt.legend()
    plt.title(title)
    if save_path:
        plt.tight_layout()
        plt.savefig(save_path)
        print(f'Saved as {save_path} in: {os.getcwd()}')

    print('Kapow. Spectra regenerated.')
    plt.show()

def write_csv(directory):
    try: 
        out_dir = os.path.join(directory, 'csv_proc')
        os.makedirs(out_dir, exist_ok = True)
        print(f'Writing to: {out_dir}')
    
        for file in os.listdir(directory):
            if file.lower().endswith(('.fits', '.fit')):
                file_path = os.path.join(directory, file)
                with fits.open(file_path) as hdul:
                    data = hdul[0].data
                    header = hdul[0].header

                print(f'ReadMultiSpec message for {file}: \n')
                print('============== \n')
                spectrum_array = readmultispec(file_path)
                print('============== \n')

                if spectrum_array is not None:
                    # print(f'I succesfully read the data in the IRAF multispec format from the WAT2 cards for {file}. \n')
                    flux = spectrum_array['flux']
                    wavelength = spectrum_array['wavelen']

                    base = os.path.splitext(file)[0]
                    output_csv = os.path.join(out_dir, f'{base}.spectrum.csv')

                    np.savetxt(output_csv, np.column_stack((wavelength, flux )), delimiter=',', header='wave,flux', comments='')
                    print(f'I successfully wrote the file {base}.spectrum.csv in {out_dir}')

        print(f'Processing finished in {directory}. \n')

    except FileNotFoundError as e:
        print(f"Error accessing '{directory}': {e} ")
        return


def generate_spectra(file_path): # make iterable on files in a directory
    """
    Generates a plot of the UV/optical spectra, obtained from the DAO.

    Args: 
        file_path: the path to the file you want to plot.

    Returns:
        None. Prints a plot. 
    
    """
    if not os.path.isfile(file_path) or not file_path.lower().endswith('.fits'):
        print(f"Error: '{file_path}' is not a valid .fits file.")
        return []
    
    try: 
        with fits.open(file_path) as hdul:
            data = hdul[0].data
            header = hdul[0].header
            # w = WCS(header, relax = True)

        ut_date = header['UT-DATE']
        target = header['OBJECT']
        instr = header['INSTRUME']

        center_wavelength = header['WAVELENG'] # central wavelength in angstroms for the data
        center_pixel = header['REFPIXEL'] - 1  # pixel where the wavelength is center wavelength (WAVELENG). python is zero base.
        delta_w = header['DELTA_WL'] # Angstrom difference per pixel. 
        c_delta = header['CDELT1'] # How many 'steps' occur between pixels. affected by binning i think?

        # try reading with readmultispec
        print('ReadMultiSpec message: \n')
        print('============== \n')
        spectrum_array = readmultispec(file_path)
        print('============== \n')

        if spectrum_array is not None:
            print('I succesfully read the data in the IRAF multispec format from the WAT2 cards. \n')
            
            flux = spectrum_array['flux']
            wavelength = spectrum_array['wavelen']

        # plotting
        pass_title = f'Spectrum of {target}: {ut_date} ({instr})'
            
        plot_spectrum(wavelength, flux, pass_title)

        # restrict domain and range

        add_lims = input(f'Restrict flux and wavelength ranges? (y/n): ').strip().lower()

        if add_lims == 'y':

            xl_lower = input(f'Enter lower wavelength limit in Angstrom ({wavelength.min()} -- {wavelength.max()}), or \'c\' to cancel: ')
            try:
                xl_lower = float(xl_lower)
            except ValueError:
                print("Invalid value.")
                xl_lower = None
            
               
            xl_upper = input(f'Enter upper wavelength limit in Angstrom ({wavelength.min()} -- {wavelength.max()}), or \'c\' to cancel: ')
            try:
                xl_upper = float(xl_upper)
            except ValueError:
                print("Invalid value.")
                xl_upper = None

            yl_lower = input(f'Enter lower flux limit in erg/cm^2/s/um ({flux.min()} -- {flux.max()}), or \'c\' to cancel: ')
            try:
                yl_lower = float(yl_lower)
            except ValueError:
                print("Invalid value.")
                yl_lower = None

            yl_upper = input(f'Enter upper flux limit in erg/cm^2/s/um ({flux.min()} -- {flux.max()}), or \'c\' to cancel: ')
            try:
                yl_upper = float(yl_upper)
            except ValueError:
                print("Invalid value.")
                yl_upper = None
           
            xlims = ([xl_lower, xl_upper])
            ylims = ([yl_lower, yl_upper])
            plot_spectrum(wavelength, flux, pass_title, xlims, ylims)

            
        elif add_lims == 'n':
            print('No changes applied.')
        else:
            print('Invalid input. I will not make changes.')

        # figure saving 

        save = input(f'Save figure? (y/n): ').strip().lower()
        supported_exts = ['.png', '.pdf', '.jpg', '.svg']

        if save == 'y':
            default_name = target.replace(" ", "_") + '_spec'
            file_name = input(f"Enter the file name if you'd like. If you press enter then I will use the default [{default_name}]: \n")
            root, ext = os.path.splitext(file_name)
            if not file_name:
                file_name = default_name
            elif ext.lower() not in supported_exts:
                print(f"I don't know that extension. just going to use .png.")
                file_name = root + '.png'
            
            # regenerate plot
            plot_spectrum(wavelength, flux, pass_title, xlims, ylims, file_name)

        elif save == 'n':
            print('I did not save a file. \n')
        else:
            print('Invalid input. I take either \'y\' or \'n\'. No file saved. \n')
        
        plt.close('all')
        
    except FileNotFoundError:
        print(f"Error: File not found in {file_path}.")
        return
    
    except TypeError as e:
        print(f"Error accessing '{file_path}': {e} ")
        return
    
    except Exception as e:
        print(f"An unexpected error occurred; {e}")
        return
    

if __name__ == "__main__":
    print("Hello from the terminal. I am the optical spectra/.csv plot producer. ")
    target_path = ""
    mkcsv = ""

    while(mkcsv != 'c'):
        mkcsv = input('Enter spectra directory to write .csv files for RASSINE normalization (c to cancel): ')

        if mkcsv.lower() == 'c':
            break
        
        write_csv(mkcsv)

    while(target_path != 'q'):
        target_path = input("Enter the .fits file path to generate DAO/optical spectra (q to quit): ")
        
        if target_path.lower() == 'q':
            break

        generate_spectra(target_path)
        print('Processing complete. \n')

    print('That is all, then. Peace be unto you.')