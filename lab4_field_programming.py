"""
GISC405 // LAB 4 // FIELD PROGRAMMING
-------------------------------------------------------------------------------
PURPOSE: IDENTIFYING VEGETATION CHANGES
-------------------------------------------------------------------------------
This script is designed to compare Normal Difference Vegetation Index (NDVI)
of two raster images (EO-1, multispectral) in Bali with different time 
(2011 and 2014) using GDAL and NumPy. Each raster is converted into set of
array then NDVI is calculated (NIR - RED / NIR + RED). After that, NDVI 
difference between both image is calculated by subtraction and result is 
converted to absolute value. The result is a new raster file which contains NDVI
value difference to identify vegetation changes where higher value (lighter 
pixel) indicating massive vegetation changes over three years period.
"""
# -----------------------------------------------------------------------------
# STEP 1: IMPORT REQUIRED PACKAGES
# -----------------------------------------------------------------------------
# Import GDAL packages
from osgeo import gdal
# Import numpy and renaming as np
import numpy as np

# -----------------------------------------------------------------------------
# STEP 2: DEFINE FUNCTION TO CALCULATE NDVI
# -----------------------------------------------------------------------------
def calcNDVI(rasterFile):
    # Register all raster read drivers
    gdal.AllRegister()
    # Open raster dataset
    inRaster = gdal.Open(rasterFile, gdal.GA_ReadOnly)
    # Get the raster red band. For EO-1 multispectral, red band is band 4
    redBand = inRaster.GetRasterBand(4) # note: counting starts at 1 for bands
    # Convert the raster red band into a NumPy array
    redArray = redBand.ReadAsArray().astype(np.float32)
    # Get the raster NIR band. For EO-1 multispectral, NIR band is band 5
    nirBand = inRaster.GetRasterBand(5) # note: counting starts at 1 for bands
    # Convert the raster NIR band into a NumPy array
    nirArray = nirBand.ReadAsArray().astype(np.float32)
    # Compute the truth value red band AND NIR band
    check = np.logical_and(redArray > 1, nirArray > 1 )  
    # Calculate NDVI
    NDVI = np.where(check, (nirArray - redArray) / (nirArray + redArray), -999)
    # Use the return function to return the NDVI value
    return(NDVI)

# -----------------------------------------------------------------------------
# STEP 3: CALCULATE NDVI CHANGE
# -----------------------------------------------------------------------------
# Get NDVI from 2011 image
NDVI2011 = calcNDVI('2011.tif')
# Get NDVI from 2014 image
NDVI2014 = calcNDVI('2014.tif')
# Calculate difference, np.abs function is necessary to convert negative to 
# positive (absolute) value
NDVIChange = np.abs(NDVI2011 - NDVI2014)

#------------------------------------------------------------------------------
# STEP 4: WRITE OUTPUT TO RASTER DATA
#------------------------------------------------------------------------------
# Register all raster read drivers
gdal.AllRegister()
# Open raster dataset
inRaster = gdal.Open('2011.tif', gdal.GA_ReadOnly)
# Get the raster's georeferencing transform
geoTransform = inRaster.GetGeoTransform()
# Get the projection information
projection = inRaster.GetProjection()
# Get the number of rows
nRows = inRaster.RasterYSize
# Get the number of columns
nCols = inRaster.RasterXSize
# Specify the driver for the output raster file type
driver = gdal.GetDriverByName('GTiff')
# Create an output raster file
outRaster = driver.Create('ndviChange.tif', nRows, nCols, 1, gdal.GDT_Float32)
# Get the output raster band
outBand = outRaster.GetRasterBand(1) # note: counting starts at 1 for bands
# Write array from ndviChange to output raster band
outBand.WriteArray(NDVIChange)
# Set the affine transformation coefficients
outRaster.SetGeoTransform(geoTransform)
# Set the projection definition string for output dataset. 
outRaster.SetProjection(projection)
# Delete the output raster file object to finalise the output file
del(outRaster)
# End of script
