
# This script is intended to calculate the total Particulate Inorganic Carbon content within the E.huxleyi bloom areas
# Pay attentinon to the input and output folders, there are placeholders there!!!

from nansat import *
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

iDir = '*Path to the input directory*'

# Loading the water and sea masks

wm = np.load(iDir + '/sea_masks/wm_array.npy')
maskBar = np.load(iDir + '/sea_masks/on_grid/npy/barentsSea.npy')
maskBer = np.load(iDir + '/sea_masks/on_grid/npy/beringSea.npy')
maskNorth = np.load(iDir + '/sea_masks/on_grid/npy/northernSea.npy')
maskNorw = np.load(iDir + '/sea_masks/on_grid/npy/norwegianSea.npy')
maskGreen = np.load(iDir + '/sea_masks/on_grid/npy/greenlandSea.npy')
maskLabr = np.load(iDir + '/sea_masks/on_grid/npy/labradorSeaFULL.npy')

# Defining the Mixed Layer Depth, Rrs, Coccolith concentration (cct) input and PIC output directories

mldDir = iDir + 'gridded/MLD/repro/Montegut_climatology/'

globcolor_mask_dir = iDir + '/gridded/spectra_mask/reprojected/globcolour/' #2017-2019
oc_cci_mask_dir = iDir + '/gridded/spectra_mask/reprojected/v3.1/'			#1998-06.2018

cctDir = '*Directory with cct*'
oDir = '*Output directory*'

# Starting to iterate years

years = range(2017,2020)

for year in years:

	year = str(year)

	# Creating the list of input files containing coccoliths concentration

	cctFiles = sorted(glob.glob(cctDir + year + '*_cct.npy'))

	# Creating the output file for writing the output
	
	f = open(oDir + 'picSum_' + year + '.txt', 'w')
	
	f.write('Date;North;Norwegian;Greenland;Barents;Bering;Labrador;All;[Tonns]\n')

	# Iterating and loading the yearly cct files and corresponding masks and MLD
	
	for cctFile in cctFiles:
	
		date = os.path.basename(cctFile)[:8]
		print date
		
		cct = np.load(cctFile)
		
		mask = np.load(globcolor_mask_dir + date + '_filled_spectra_mask_glob_colour_with_nan_531.npy') # GlobColor

		mld = np.load(mldDir + date[4:6] + '.npy')
		
		# Calculating the volume cct content withing the bloom mask

		cctVolume = np.zeros(cct.shape)
		cctVolume[(wm==0)&(np.isnan(cct)==0)&(mld!=1e+09)&(np.isnan(mld)==0)*(mask==1)] = cct[(wm==0)&(np.isnan(cct)==0)&(mld!=1e+09)&(np.isnan(mld)==0)*(mask==1)]*mld[(wm==0)&(np.isnan(cct)==0)&(mld!=1e+09)&(np.isnan(mld)==0)*(mask==1)]
		
		# Calculating the PIC values withing the bloom mask

		pic = cctVolume*0.0032 #in [Tonns]
		pic[wm==1]=np.nan

		# Saving and plotting the result
		
		np.save(oDir + date + '_pic.npy', pic)
		
		plt.imshow(pic, vmin=0, vmax=50)
		plt.colorbar()
		plt.title('PIC concentration in tonns')
		plt.savefig(oDir + date + '_pic.png', dpi=200)
		plt.close()
		
		# Calculating the total PIC content within the bloom for each sea

		picSumNorth = np.nansum(pic[maskNorth==1])
		picSumNorw = np.nansum(pic[maskNorw==1])
		picSumGreen = np.nansum(pic[maskGreen==1])
		picSumBar = np.nansum(pic[maskBar==1])
		picSumBer = np.nansum(pic[maskBer==1])
		picSumLabr = np.nansum(pic[maskLabr==1])
		picSumAll = picSumNorth+picSumNorw+picSumGreen+picSumBar+picSumBer+picSumLabr

		# Writing the result
		
		f.write(date + ';' + str(picSumNorth) + ';' +
							 str(picSumNorw) + ';' +
							 str(picSumGreen) + ';' +
							 str(picSumBar) + ';' +
							 str(picSumBer) + ';' +
							 str(picSumLabr) + ';' +
							 str(picSumAll) + '\n')
		
	f.close()
	
