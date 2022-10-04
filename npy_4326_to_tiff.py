
# This script is intended to create geoTiff file containing the geospatial metadata from npy array with bathymetry values in known projection (EPSG 4326, full domain, 4320x8640)
# Pay attentinon to the input and output folders, there are placeholders there!!!

from osgeo import gdal
import osgeo.gdalconst
import numpy as np

# Defining the array

seas_array = np.load('*Path to the bathymetry file*/elevation_global_4320x8640.npy') #set your npy array here

# Preparing the GeoTiff file using official proj metadata and writing array to its first band

driver = gdal.GetDriverByName("GTiff")

proj = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,UTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]' # Official proj for EPSG:4326

geo = (-180.0000051, 0.041666666666666664, 0.0, 90, 0.0, -0.041666666666666664) # Parameters: top left longitude, resolution, rotate, top left latitude, rotate, res

outData = driver.Create('*Path to your file*/bathymetry_4326.tif', 8640, 4320, 1, gdal.GDT_Float32 ) # Set output path here
outData.SetProjection(proj)
outData.SetGeoTransform(geo)
outData.GetRasterBand(1).WriteArray(seas_array)
outData = None
