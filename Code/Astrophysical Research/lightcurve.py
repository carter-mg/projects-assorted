from astropy.io import fits
from astropy.time import Time
from astropy.coordinates import EarthLocation, SkyCoord
import astropy.units as u

import lightkurve as lk
import matplotlib.pyplot as plt

from lightkurve import search_targetpixelfile
from lightkurve import search_lightcurve

#Import lightcurve data
search= lk.search_lightcurve("V927 Her")

v927a = search[0].download().remove_outliers()

v927a.plot();

#Pull metadata
lc_date_start = v927a.meta.get("DATE-OBS")
lc_time_start = v927a.meta.get("TSTART")
lc_time_stop = v927a.meta.get("TSTOP")
lc_date_end = v927a.meta.get("DATE-END")

#Accessing data from object
times = v927a.time
times_jd = times.jd

print(f"Time format: {times.format}")
print(f"Times in Julian: {times_jd}")
print(f"Time Start: {lc_time_start}")

#Converting BTJD to BJD 
#from https://spacetelescope.github.io/notebooks/notebooks/MAST/TESS/beginner_how_to_use_ffi/beginner_how_to_use_ffi.html

lc_time_start_bjd = lc_time_start - 2457000
lc_time_stop_bjd = lc_time_stop - 2457000

print(f"Start / Stop times in BJD: \n {lc_time_start_bjd} / {lc_time_stop_bjd} ")

#Plot lightcurve
period = v927a.to_periodogram("bls").period_at_max_power
print(f"Period at Max Power: {period}")

# setting fonts
plt.rcParams['font.family'] = 'Times New Roman'

# plot

folded = v927a.fold(period).scatter()

# viewing
ax = folded.plot()
plt.xlabel('Phase (JD)')
plt.ylabel('Flux (e$^{-}$ s $^{-1}$)')
plt.xlim(0, .17)
plt.title("V927 Folded Lightcurve")

