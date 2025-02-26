#Normalizing

#Libraries
import astropy.units as u
from astropy.io import fits
from specutils import Spectrum1D
from specutils.fitting import fit_generic_continuum
import matplotlib.pyplot as plt
import os
import numpy as np

#Set working directory
os.chdir('C:/Users/cmark/Onedrive/Documents/TUIExposures')

print(os.getcwd())

#Open .fits file and get data
with fits.open('V927Her.fmerged.fits') as hdul:
    data = hdul[0].data

    wavelength = data[0]
    flux = data[1]
    
    # Remove non-finite values
    finite_mask = np.isfinite(wavelength) & np.isfinite(flux)
    wavelength = wavelength[finite_mask]
    flux = flux[finite_mask]
    
spectrum = Spectrum1D(flux=flux * u.Unit('erg / (cm^2 s Angstrom)'), spectral_axis=wavelength * u.AA)

# Trying the continuum
try: 
    continuum = fit_generic_continuum(spectrum)
except Exception as e: 
    print(f"Ereror fitting continuum: {e}")

# Fit the continuum
#continuum = fit_generic_continuum(spectrum)

#Apply th fit to obstain th normalized spectrum 
model = continuum(spectrum.spectral_axis)
normalized_spectrum = spectrum / model

# Plot spectrum
plt.figure(figsize=(10, 6))
plt.plot(spectrum.spectral_axis, spectrum.flux, label='Original Spectrum')
plt.plot(spectrum.spectral_axis, normalized_spectrum.flux, label='Normalized Spectrum', linestyle='--')
#plt.plot(model, label='Model Spectrum')
plt.xlabel('Wavelength (Microns)')
plt.ylabel('Flux')
plt.legend()
plt.show()