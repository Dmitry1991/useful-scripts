# useful-scripts
This is a repository containing some useful scripts that I used during my work

Here are some name descriptions:

- npy_4326_to_tiff.py is intended to create geoTiff file containing the geospatial metadata from npy array with bathymetry values in known projection (EPSG 4326, full domain, 4320x8640)

- sst_repro.py is intended to reproject the input NASA Sea Surface Temperature (SST) satellite images in netCDF format to the chosen projection using gdal library

- sst_4day_average.py is intended to average the reprojected Sea Surface Temperature netCDF files over 4 days intervals

- pic_calc.py is intended to calculate the total Particulate Inorganic Carbon content within the E.huxleyi bloom areas

- delta_pCO2_calc.py is intended to calculate the delta_pCO2 values in water within the bloom areas based on the regression dependence on values of Rrs490

- pp_cal.py is intended to calculate the Primary Production values based on Chlorophyll concentration values obtained from diferent sources (Case1 NASA chl and two BOREALI models)
