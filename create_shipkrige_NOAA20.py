"""
Create input data for kriging from NOAA20 VIIRS data

Testing for Houthi crisis analysis

Modifications
-------------
20 December 2024: Michael Diamond, Tallahassee, FL
    -Created
"""

#Import libraries
import numpy as np
import xarray as xr
from scipy import stats
import matplotlib.pyplot as plt
from glob import glob
import os
import warnings

#Set paths
dir_data = '/Users/michaeldiamond/Documents/Data/'

"""
Create shipkrige nc file for R kriging code
"""

sk = xr.Dataset()

#Load legacy shipkrige file from Diamond et al. (2020), AGU Adv.
orig = xr.open_dataset('/Users/michaeldiamond/Dropbox/ShipTrackAnalysis_MichaelDiamond/origData/shipkrige_combinedvars.nc')
sk['month'] = orig['month']
sk['lat'] = orig['lat']
sk['lon'] = orig['lon']
sk['EDGAR_SO2'] = orig['EDGAR_SO2']

#
###Load and manipulate NOAA20 VIIRS data
#

#Load Nad data
for year in range(2018,2024+1): sk[f'NOAA20_Nad_{year}'] = (['month','lat','lon'], np.nan*np.ones((12,180,360)))

flist = sorted(glob(dir_data+'VIIRS/*NOAA20*'))

cot_bounds = np.array([0., 2., 4., 6., 8., 10., 15., 20., 30., 40., 50., 100., 150.])
cer_bounds = np.array([4., 6., 8., 10., 12.5, 15., 17.5, 20., 25., 30.])

cot = (cot_bounds[:-1]+cot_bounds[1:])/2
cer = (cer_bounds[:-1]+cer_bounds[1:])/2

c = 1.4067*1e-6 #cm-1/2
tau, ref = np.meshgrid(cot,cer)
nd = np.array(c*tau**(1/2)*(ref*1e-4)**(-5/2))[:,:,np.newaxis,np.newaxis]

for i, year in zip(np.arange(len(flist))[::2],np.arange(2018,2024+1)):
    print(year)
    
    #September
    f = flist[i]
    jhist = xr.open_dataset(f,group='Cloud_Optical_Thickness_Liquid')['JHisto_vs_Eff_Radius']
    Nad = np.nansum(nd*jhist.T.values,axis=(0,1))/np.nansum(jhist.T.values,axis=(0,1))
    sk[f'NOAA20_Nad_{year}'][9-1][:] = Nad[::-1]
    
    #October
    f = flist[i+1]
    jhist = xr.open_dataset(f,group='Cloud_Optical_Thickness_Liquid')['JHisto_vs_Eff_Radius']
    Nad = np.nansum(nd*jhist.T.values,axis=(0,1))/np.nansum(jhist.T.values,axis=(0,1))
    sk[f'NOAA20_Nad_{year}'][10-1][:] = Nad[::-1]

#Load SST data
for year in range(2018,2024+1): sk[f'ERSST_{year}'] = (['month','lat','lon'], np.nan*np.ones((12,180,360)))

flist = sorted(glob(dir_data+'ERSST/*'))

for i, year in zip(np.arange(len(flist))[::2],np.arange(2018,2024+1)):
    print(year)
    
    #September
    f = flist[i]
    ersst_ = xr.open_dataset(f)['sst'][0,0]
    ersst = ersst_.interp(lat=sk.lat,lon=np.arange(.5,360),method='linear',kwargs={"fill_value": "extrapolate"})

    sk[f'ERSST_{year}'][9-1][:,180:] = ersst[:,:180].values
    sk[f'ERSST_{year}'][9-1][:,:180] = ersst[:,180:].values
    
    #October
    f = flist[i+1]
    ersst_ = xr.open_dataset(f)['sst'][0,0]
    ersst = ersst_.interp(lat=sk.lat,lon=np.arange(.5,360),method='linear',kwargs={"fill_value": "extrapolate"})

    sk[f'ERSST_{year}'][10-1][:,180:] = ersst[:,:180].values
    sk[f'ERSST_{year}'][10-1][:,:180] = ersst[:,180:].values


###Save file
#

filename = dir_data+'/VIIRS/NOAA20_shipkrige.nc'
os.system('rm %s' % filename) #Delete file if it already exists
sk.to_netcdf(path=filename,mode='w')

