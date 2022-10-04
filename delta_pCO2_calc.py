
# This script is intended to calculate the delta_pCO2 values in water within the bloom areas based on the regression dependence on values of Rrs490
# Pay attentinon to the input and output folders, there are placeholders there!!!

import glob
import numpy as np
import os
from osgeo import gdal
import matplotlib.pyplot as plt

# Defining the slope and intercept values from previously obtained regression between delta_pCO2 and Rrs490

slope=0.00013833173418845615
intercept=0.008285659160846082

# Loading the water mask

wm = np.load('*Insert the path to the water mask here*')

# Loading the sea masks

barents_mask = np.load('*Insert the path to the sea mask here*')
bering_mask = np.load('*Insert the path to the sea mask here*')
north_mask = np.load('*Insert the path to the sea mask here*')
norwegian_mask = np.load('*Insert the path to the sea mask here*')
greenland_mask = np.load('*Insert the path to the sea mask here*')
labrador_mask = np.load('*Insert the path to the sea mask here*')
black_mask = np.load('*Insert the path to the sea mask here*')

# Defining the list of input filenames

iFiles = sorted(glob.glob('*Insert the path to the input files here*/????????_rrs_filled.tif'))

# Opening the .txt file to write the ouput

f = open('*Insert the path to the output file here*.txt', 'w')
f.write('date;north_mean;norwegian_mean;greenland_mean;barents_mean;bering_mean;labrador_mean;black_mean;north_max;norwegian_max;greenland_max;barents_max;bering_max;labrador_max;black_max;\n')

# Starting the iteration of files

for iFile in iFiles:
	
	filename = os.path.basename(iFile)
	date = filename[:8]
	
	print 'processing ' + date + '...'
	

	# Reading the Rrs490 array from GeoTiff file

	n = gdal.Open(iFile, gdal.GA_ReadOnly)
	Rrs_490 = n.GetRasterBand(3).ReadAsArray()

	# Loading the bloom mask

	mask = np.load('*Insert the path to the bloom mask here*' + date + '_filled_spectra_mask.npy')

	# Calculating the delta_pCO2 values within the bloom mask

	delta_pCO2 = np.zeros(Rrs_490.shape)
	delta_pCO2[wm==1] = np.nan
	delta_pCO2[(mask==1)&(wm==0)] = (Rrs_490[(mask==1)&(wm==0)]-intercept)/slope
	
	# Plotting and saving the delta_pCO2 values

	plt.imshow(delta_pCO2,vmin = 0,vmax=250)
	plt.colorbar()
	plt.savefig('*Insert the path to the output images here*'+date+'_delta_pco2_not_corrected.png', dpi=300)
	plt.close()

	# STARTING THE CORRECTION PROCEDURE
	
	# Loading the Sea Surface Temperature and Salinity arrays for current date
	
	sst = np.load('*Insert the path to the SST file here*' + date + '.npy')
	sss = np.load('*Insert the path to the SSS file here*' + date[4:6] + '.npy')
	
	# Defining the correction coefficients according to the (Copin-Montegut et al., 1988) and initiating the correction

	alpha = (-1090+7*sss)*(10**(-6))
	A = (3695+9*sss)*(10**(-5))
	B = (389 + 2.2*sss)*(10**(-6))
	C=(0.34-0.124*sss)*(10**(-6))
	
	a = 1+alpha*sst
	b = 1+A*sst+B*(sst**2)+C*(sst**3)
	
	ai = 1+alpha*10
	bi = 1+A*10+B*(10**2)+C*(10**3)
	
	lnf = (a/ai)*(np.log((delta_pCO2/bi)))+np.log(b)
	
	delta_pco2_corrected = np.e**(lnf)
	
	# Saving and plotting the obtained result

	np.save('*Insert the path to the output file here*'+date+'_delta_pco2.npy', delta_pco2_corrected)
	
	plt.close()
	plt.imshow(delta_pco2_corrected,vmin = 0,vmax=250)
	plt.colorbar()
	plt.savefig('*Insert the path to the output file here*'+date+'_delta_pco2_corrected.png', dpi=300)
	plt.close()
	
	# Calculating the max and mean values along the bloom area in each sea (if the respective values is less than the error value, assigning zero value)

	if (delta_pco2_corrected[(north_mask==1)&(mask==1)&(wm==0)].shape[0]!=0)&(np.sum(np.isnan(delta_pco2_corrected[(north_mask==1)&(mask==1)&(wm==0)])==0)>50):
		north_max = np.nanmax(delta_pco2_corrected[(north_mask==1)&(mask==1)&(wm==0)])
		if north_max<24.0:
			north_max=0.0
		north_mean = np.nanmean(delta_pco2_corrected[(north_mask==1)&(mask==1)&(wm==0)])
		if north_mean<24.0:
			north_mean=0.0
	else:
		north_max = 0.0
		north_mean = 0.0
	if (delta_pco2_corrected[(norwegian_mask==1)&(mask==1)&(wm==0)].shape[0]!=0)&(np.sum(np.isnan(delta_pco2_corrected[(norwegian_mask==1)&(mask==1)&(wm==0)])==0)>50):	
		norwegian_max = np.nanmax(delta_pco2_corrected[(norwegian_mask==1)&(mask==1)&(wm==0)])
		if norwegian_max<24.0:
			norwegian_max=0.0
		norwegian_mean = np.nanmean(delta_pco2_corrected[(norwegian_mask==1)&(mask==1)&(wm==0)])
		if norwegian_mean<24.0:
			norwegian_mean=0.0
	else:
		norwegian_max = 0.0
		norwegian_mean = 0.0
	if (delta_pco2_corrected[(greenland_mask==1)&(mask==1)&(wm==0)].shape[0]!=0)&(np.sum(np.isnan(delta_pco2_corrected[(greenland_mask==1)&(mask==1)&(wm==0)])==0)>50):	
		greenland_max = np.nanmax(delta_pco2_corrected[(greenland_mask==1)&(mask==1)&(wm==0)])
		if greenland_max<24.0:
			greenland_max=0.0
		greenland_mean = np.nanmean(delta_pco2_corrected[(greenland_mask==1)&(mask==1)&(wm==0)])
		if greenland_mean<24.0:
			greenland_mean=0.0		
	else:
		greenland_max = 0.0
		greenland_mean = 0.0
	if (delta_pco2_corrected[(barents_mask==1)&(mask==1)&(wm==0)].shape[0]!=0)&(np.sum(np.isnan(delta_pco2_corrected[(barents_mask==1)&(mask==1)&(wm==0)])==0)>50):	
		barents_max = np.nanmax(delta_pco2_corrected[(barents_mask==1)&(mask==1)&(wm==0)])
		if barents_max<24.0:
			barents_max=0.0
		barents_mean = np.nanmean(delta_pco2_corrected[(barents_mask==1)&(mask==1)&(wm==0)])
		if barents_mean<24.0:
			barents_mean=0.0		
	else:
		barents_max = 0.0
		barents_mean = 0.0
	if (delta_pco2_corrected[(bering_mask==1)&(mask==1)&(wm==0)].shape[0]!=0)&(np.sum(np.isnan(delta_pco2_corrected[(bering_mask==1)&(mask==1)&(wm==0)])==0)>50):	
		bering_max = np.nanmax(delta_pco2_corrected[(bering_mask==1)&(mask==1)&(wm==0)])
		if bering_max<24.0:
			bering_max=0.0
		bering_mean = np.nanmean(delta_pco2_corrected[(bering_mask==1)&(mask==1)&(wm==0)])
		if bering_mean<24.0:
			bering_mean=0.0		
	else:
		bering_max = 0.0
		bering_mean = 0.0
	if (delta_pco2_corrected[(labrador_mask==1)&(mask==1)&(wm==0)].shape[0]!=0)&(np.sum(np.isnan(delta_pco2_corrected[(labrador_mask==1)&(mask==1)&(wm==0)])==0)>50):	
		labrador_max = np.nanmax(delta_pco2_corrected[(labrador_mask==1)&(mask==1)&(wm==0)])
		if labrador_max<24.0:
			labrador_max=0.0
		labrador_mean = np.nanmean(delta_pco2_corrected[(labrador_mask==1)&(mask==1)&(wm==0)])
		if labrador_mean<24.0:
			labrador_mean=0.0		
	else:
		labrador_max = 0.0
		labrador_mean = 0.0	
	if (delta_pco2_corrected[(black_mask==1)&(mask==1)&(wm==0)].shape[0]!=0)&(np.sum(np.isnan(delta_pco2_corrected[(black_mask==1)&(mask==1)&(wm==0)])==0)>50):	
		black_max = np.nanmax(delta_pco2_corrected[(black_mask==1)&(mask==1)&(wm==0)])
		if black_max<24.0:
			black_max=0.0
		black_mean = np.nanmean(delta_pco2_corrected[(black_mask==1)&(mask==1)&(wm==0)])
		if black_mean<24.0:
			black_mean=0.0		
	else:
		black_max = 0.0
		black_mean = 0.0	
	
	# Writing the calculated values for each sea to the output file
		
	f.write(date+';'+str(north_mean)+';'+str(norwegian_mean)+';'+str(greenland_mean)+';'+str(barents_mean)+';'+str(bering_mean)+';'+str(labrador_mean)+';'+str(black_mean)+';'+str(north_max)+';'+str(norwegian_max)+';'+str(greenland_max)+';'+str(barents_max)+';'+str(bering_max)+';'+str(labrador_max)+';'+str(black_max)+'\n')
	
f.close()
