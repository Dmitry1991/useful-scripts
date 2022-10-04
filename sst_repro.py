
# This script is intended to reproject the input NASA Sea Surface Temperature (SST) satellite images in netCDF format to the chosen projection using gdal library
# Pay attentinon to the input and output folders, there are placeholders there!!!

from datetime import datetime
startTime = datetime.now()
import subprocess
from nansat import *
import os
import glob
import numpy as np

# Defining the input and output directories

iDir = '*Input directory path*'
oDir = '*Output directory path*'

# Listing the input files with SST

iFiles = sorted(glob.glob(iDir + '201*_day-v02.0-fv01.0.nc'))

# Starting the iteration process

for iFile in iFiles:
	
	# Checking if the file is already reprojected

	fileName = os.path.split(iFile)[1]
	print fileName
	
	if os.path.exists(oDir + fileName[0:8] + '_sst_repro.nc'):
		continue
	else:

		# Reprojection command
		gdalCommand = 'gdalwarp -wo SAMPLE_GRID=YES -wo SAMPLE_STEPS=1000 -t_srs EPSG:3973 -te -5000000 -5000000 5000000 5000000 -tr 4000 4000 -overwrite -of netCDF'
		
		# Defining input and output files
		inputFile = 'NETCDF:"' + iFile + '":' + 'sea_surface_temperature'
		outputFile = oDir + fileName[0:8] + '_sst_repro.nc'
		
		# Converting the command to the list of strings
		gdalCommandList = gdalCommand.split(' ')

		# Adding the input and output files to the list
		gdalCommandList += [inputFile, outputFile]

		# Executing the command
		status = subprocess.call(gdalCommandList)
	
print 'finished in ' + str(datetime.now() - startTime)
