# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 01:38:38 2025

@author: MrAdmin
"""
#handlin geotiff
#lo siguiente asume que esta el geotiff bajado a la carpeta de este mismo prjecto

import rasterio
import matplotlib.pyplot as plt
#import geopandas
#import shapely
import numpy as np
 
gpw_file = r'C:\Users\Ernest\OneDrive\Desktop\Population Project\gpw-v4-population-count-adjusted-to-2015-unwpp-country-totals-rev11_2020_1_deg_tif\gpw_v4_population_count_adjusted_to_2015_unwpp_country_totals_rev11_2020_1_deg.tif'


def load_population_data(file):
    with rasterio.open(file) as src:
        # Read band 1 as a float32 NumPy array
        data = src.read(1).astype(np.float32)
        nodata = src.nodata
        if nodata is not None:
            data = np.where(data == nodata, np.nan, data)
    return data

population = load_population_data(gpw_file)

plt.imshow(population, cmap="viridis")
plt.colorbar(label="Population Count")
plt.title("GPWv4 Adjusted Population Count")
plt.show()

def process_and_save_data(file, output_file):
    with rasterio.open(file) as src:
        data = src.read(1).astype(np.float32)
        nodata = src.nodata
        if nodata is not None:
            data = np.where(data == nodata, np.nan, data)
            np.save(output_file, data)
            
process_and_save_data(gpw_file, 'array_from_tif')