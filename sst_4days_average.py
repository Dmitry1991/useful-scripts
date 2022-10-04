
# This script is intended to average the reprojected Sea Surface Temperature netCDF files over 4 days intervals
# Pay attentinon to the input and output folders, there are placeholders there!!!

import datetime
import subprocess
import os
import glob
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt

# Defining the input and output folders

iDir = '/nfs0/dmitryk/sst_pathfinder_repro/'
oDir = '/nfs0/dmitryk/sst_pathfinder_repro/4days/'

# Defining the starting date

date = datetime.datetime(2010,1,16)
td = datetime.timedelta(days=1)

# Iterating dates until year 2018

while date.year < 2018:

	# Creating empty list for appending the daily SST arrays

    four_days_list = []
    four_days_date = date.strftime(format = '%Y%m%d')
    print 'Current 4-days date is ' + four_days_date
    
	# Cheking if the date is already processed

    if os.path.exists(oDir + four_days_date + '_4days_sst.npy'):
        print 'Date ' + four_days_date + ' already exists. Continue with next date...'
        date = date + datetime.timedelta(days=4)
    else:

        for i in range(1,5):
            
            current_date = date.strftime(format = '%Y%m%d')
            print 'Processing ' + current_date + '...'
            
			# Trying to process the date (if it is not corrupted or absent)

            try:
                
				# Loading the SST and mask and flipping it northwards

                sst_ds = Dataset(iDir + current_date + '_sst_repro.nc')
                sst_mask_ds = Dataset(iDir + current_date + '_sst_repro_mask.nc')
                
                sst = np.flipud(sst_ds.variables['Band1'][:])
                mask = np.flipud(sst_mask_ds.variables['Band1'][:])
        
				# Dropping the bad values from SST and converting it to the real values (using standard NASA SST slope = 0.01)
				
                sst = sst.astype(float)
                sst[sst==-32768.]=np.nan
                sst = 0.01*sst
                sst[mask!=7]=np.nan
                
				# Plotting the daily SST and appending them to the 4-days list
	
                plt.imshow(sst)
                plt.colorbar()
                plt.savefig('/nfs0/dmitryk/sst_pathfinder_repro/' + current_date + '_daily_sst.png')
                plt.close()
                
                four_days_list.append(sst)
                date = date + td
            
            except:
                print current_date + ' is corrupted. Continue with next date...'
                date = date + td
                
        print '4 days ended. Averaging...'
        
		# Averaging the 4-days arrays and saving and plotting the result

        four_days_array = np.array(four_days_list)
        sst_4day_mean = np.nanmean(four_days_array, axis = 0)
        np.save(oDir + four_days_date + '_4days_sst.npy', sst_4day_mean)
        
        plt.imshow(sst_4day_mean)
        plt.colorbar()
        plt.savefig(oDir + four_days_date + '_4days_sst.png')
    
