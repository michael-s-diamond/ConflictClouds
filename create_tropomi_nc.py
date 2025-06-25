"""
Create netCDF files from ASCII $\mathrm{NO}_2$ data: Sept-Oct 2018-2024
"""

#Load libraries
import numpy as np
import xarray as xr
from glob import glob

#Get ascii files
files = sorted(glob('/Users/michaeldiamond/Documents/Data/TROPOMI/no2_*.asc'))
years = [file[-10:-6] for file in files]
months = [file[-6:-4] for file in files]

#Set up DataArray for netCDF
ds = xr.Dataset()
ds['time'] = [np.datetime64(f'{year}-{month}-15T12:00') for year, month in zip(years, months)]
ds['lat'] = np.arange(-90+0.125/2,90,0.125)
ds['lon'] = np.arange(-180+0.125/2,180,0.125)
ds['NO2'] = (['time','lat','lon'],np.nan*np.ones((len(ds.time),1440,2880)))
ds['NO2'].attrs = {'units' : '10^15 molecules cm-2'}

#Infill data
for i in range(len(files)):
    file = files[i]
    print(file)
    data = open(file).read()

    for j in range(1,1440):
        if j%200==0: print(ds.lat[j].values)

        lines = data.split('lat=')[j].split('\n')[1:-1]

        ds['NO2'][i,j][:] = np.array([[int(line[k*4:k*4+4]) for k in range(20)] for line in lines]).ravel()/100

#Save file
ds.to_netcdf('/Users/michaeldiamond/Documents/Data/TROPOMI/no2_temis_201809-202410.nc')
