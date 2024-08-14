import matplotlib.pyplot as plt
import os
from astropy.io import fits
from astropy.time import Time
from astropy.coordinates import EarthLocation, SkyCoord
import astropy.units as u
import lightkurve as lk

# Set working directory
os.chdir('C:/Users/cmark/Onedrive/Documents/TUIExposures')
print(os.getcwd())

#Readability
print("-------------------APO Calculations-------------------")

# Open .fits file
with fits.open('V927Her.fmerged.fits') as hdul:
    header = hdul[0].header
    
# Get necessary dates and times from .fits file
obs_start_time = header['SRT_TIME']
obs_end_time = header['END_TIME']
obs_date = header['SRT_DATE']

print(f"APO Observation Start: {obs_start_time}")
print(f"APO Observation Date: {obs_date}")

observation_time = obs_date + 'T' + obs_start_time
print(f"Formatted Observation Time: {observation_time}")

# Convert time to Julian
t = Time(observation_time, format='isot', scale='utc')
julian_date = t.jd
print(f"APO Observation Julian Date: {julian_date}")

# Set location (Apache Point Observatory coordinates)
location = EarthLocation.from_geodetic(lon=-105.820417 * u.deg, lat=32.780361 * u.deg, height=2788 * u.m)
print(f"APO Earth Location Coordinates: {location}")

# Coordinates of target
star_coord = SkyCoord(ra=17.9985124872 * u.deg, dec=35.856677532 * u.deg, frame='icrs')
#print(f"Star Coordinates: {star_coord}")

# Converting to Barycentric Julian Date, might be off. 
bjd = t.light_travel_time(star_coord, location=location).jd + julian_date
print(f"Barycentric Julian Date of APO Observation: {bjd}")


#LIGHTCURVE DATA
#Readability
print("-------------------LIGHTCURVE CALCULATIONS-------------------")

# Load a light curve file 
search= lk.search_lightcurve("V927 Her")

lc = search[0].download().remove_outliers()

#Pull metadata
lc_date_start = lc.meta.get("DATE-OBS")
lc_date_end = lc.meta.get("DATE-END")
lc_time_start = lc.meta.get("TSTART")
lc_time_stop = lc.meta.get("TSTOP")

print(f"Observation Time Start (Lightcurve, BTJD): {lc_time_start}")
print(f"Observation Time End (Lightcurve, BTJD): {lc_time_stop}")
print(f"Observation Date Start (Lightcurve, ISOT): {lc_date_start}")
print(f"Observation Date End (Lightcurve, ISOT): {lc_date_end}")

# Find maximum light with time. 
max_flux = lc.flux.max()
max_time = lc.time[lc.flux.argmax()]
max_time_jd = max_time.jd


print(f"The maximum flux is {max_flux} at time {max_time_jd}")
plt.figure()
lc.plot()
plt.plot(max_time.value, max_flux.value, 'ro', label='Maximum Flux')
plt.legend()
plt.show()

# Convert lightcurve times to Julian Date. Gets to Barycentric Dynamical Time.
if lc_time_start:
    t_start_lc = Time(lc_date_start, format='isot', scale='utc')
    julian_date_start_lc = t_start_lc.tdb
    print(f"Julian Date Start (Lightcurve): {julian_date_start_lc}")

if lc_time_stop:
    t_end_lc = Time(lc_date_end, format='isot', scale='utc')
    julian_date_end_lc = t_end_lc.tdb
    print(f"Julian Date End (Lightcurve): {julian_date_end_lc}")

# Calculate phase of the star
# Period of V927 Her, from SIMBAD Data. Period_at_max_light from lighkurve gives a value that is 3x the known period
period = 0.130530 
phase = ((bjd - max_time_jd) % period) / period
print("-------------------V927 Her Phase-------------------")
print(f"Phase of the star: {phase}")
