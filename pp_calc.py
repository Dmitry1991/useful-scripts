
# This script is intended to calculate the Primary Production values based on Chlorophyll concentration values obtained from diferent sources (Case1 NASA chl and two BOREALI models)
# Pay attentinon to the input and output folders, there are placeholders there!!!

from netCDF4 import Dataset
import datetime
import numpy as np
from osgeo import gdal
import math
from calendar import monthrange
import matplotlib.pyplot as plt

# Defining the input folder

iDir = '*Define the path to all the input files*'

# Loading the latitude values and their mask

lats_ds = Dataset(iDir + 'lat_repro.nc')
lats = np.flipud(lats_ds.variables['Band1'][:].data)
mask = np.flipud(lats_ds.variables['Band1'][:].mask)

# Starting to iterate the years and months

for year in range(2003,2021):
	
	for month in range(3,11):

		# Calculating the julian date		

		date = str(year) + str(month).zfill(2)
		print date
		datetime.datetime(year, month, 15).strftime('%j')
		
		julian_day = int(datetime.datetime(year, month, 15).strftime('%j'))

		# Calculating daylength (don't change this)

		if year%4==0:
			date_angle_rad = np.deg2rad(360*julian_day/366)
		else:
			date_angle_rad = np.deg2rad(360*julian_day/365)

		decl_deg = 0.39637-22.9133*np.cos(date_angle_rad)+4.02543*np.sin(date_angle_rad)-0.3872*np.cos(2*date_angle_rad)+0.052*np.cos(2*date_angle_rad)
		decl_rad = np.deg2rad(decl_deg)

		lat_rad = np.deg2rad(lats)

		daylength = 0.133*np.rad2deg(np.arccos(-np.tan(lat_rad)*np.tan(decl_rad)))
		daylength[(np.isnan(daylength)==1)&(np.absolute(-np.tan(lat_rad)*np.tan(decl_rad))!=-np.tan(lat_rad)*np.tan(decl_rad))] = 24
		daylength[(np.isnan(daylength)==1)&(np.absolute(-np.tan(lat_rad)*np.tan(decl_rad))==-np.tan(lat_rad)*np.tan(decl_rad))] = 0
		daylength[mask==True] = np.nan

		#End of calculating daylength

		# Loading the necessary arrays (SST, PAR, Chl, Kd490). Pay attention to the filepaths!

		sst_ds = Dataset(iDir + 'sst/repro/' + date + '_sst.nc')
		sst = np.flipud(sst_ds.variables['Band1'][:].data)

		sst_mask_ds = Dataset(iDir + 'sst/repro/' + date + '_mask.nc')
		sst_mask = np.flipud(sst_mask_ds.variables['Band1'][:].data)

		sst = sst.astype(float)
		sst[sst==-32767]=np.nan
		sst[sst_mask!=0]=np.nan
		sst = sst*0.005

		par_ds = gdal.Open(iDir + '/par/repro/' + date + '_par_repro.tif', gdal.GA_ReadOnly)
		par =  par_ds.GetRasterBand(1).ReadAsArray()

		# Chl1 is default, NASA has the Chl for case2 waters, but it is reduced in timespan!

		chl1_ds = gdal.Open(iDir + '/chl1/repro/' + date + '_chl1_repro.tif', gdal.GA_ReadOnly)
		chl1 =  chl1_ds.GetRasterBand(1).ReadAsArray()

		#chl2_ds = gdal.Open(iDir + '/chl2/repro/' + date + '_chl2_repro.tif', gdal.GA_ReadOnly)
		#chl2 =  chl2_ds.GetRasterBand(1).ReadAsArray()

		kd_490_ds = gdal.Open(iDir + '/kd_490/repro/' + date + '_kd_490_repro.tif', gdal.GA_ReadOnly)
		kd_490 =  kd_490_ds.GetRasterBand(1).ReadAsArray()

		# Calculating the p_opt values according to the Behrenfeld & Falkowski algorithm:

		p_opt = 3.27*10**(-8)*sst**7 + 3.4132*10**(-6)*sst**6 + 1.348*10**(-4)*sst**5 + 2.462*10**(-3)*sst**4 - 0.0205*sst**3 + 0.0617*sst**2 + 0.2749*sst + 1.2956	# (mg C mg(chl)^-1 hour^-1)

		# Calculating the euphotic depth
		
		z_eu = math.log(0.01)/kd_490	# (m)

		# Calculating the overall daily primary production 

		pp_eu_daily = 0.66125 * p_opt * (par/(par + 4.1)) * (abs(z_eu)) * chl1 * daylength	# chl1 or chl2 (mgC day^-1 m^-2)
		
		# Calculating the monthly primary production

		pp_eu_monthly = (pp_eu_daily*monthrange(year, month)[1])/1000 # (g C month^-1 m^-2)

		# Saving and plotting the result

		np.save(iDir + 'pp/' + str(year) + str(month).zfill(2) + '_pp.npy', pp_eu_monthly)
		plt.imshow(pp_eu_monthly, vmax = 3000); plt.colorbar(); plt.savefig(iDir + 'pp/' + str(year) + str(month).zfill(2) + '_pp.png'); plt.close()
