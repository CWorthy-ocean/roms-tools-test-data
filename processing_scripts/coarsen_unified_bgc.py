import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

# This script is used to coarsen the current UNIFIED BGC dataset to make a new coarse dataset used for testing.

path_2_bgc = './BGCdataset_v2_filled.nc'  # just tracking which file we are at for the test file
path_2_coarsened_bgc = './coarsened_UNIFIED_bgc_dataset.nc'

# Load in both datasets
bgc = xr.open_dataset(path_2_bgc, decode_times=False)
bgc_coarse = xr.open_dataset(path_2_coarsened_bgc, decode_times=False)

# Interpolate the full BGC dataset onto the coords of the coarsened dataset. Interpolation is used
# since downsampling doesn't align on the the same lat, lon coords as the previous coarsened file. 
bgc_interp = bgc.swap_dims({"lat": "latitude", "lon": "longitude"}).interp(
    latitude=bgc_coarse.latitude,
    longitude=bgc_coarse.longitude,
)

bgc_interp = bgc_interp.reset_coords('latitude')
bgc_interp = bgc_interp.reset_coords('longitude')

# Reduce the depth to the first 2, to provide surface data needed during testing.
bgc_interp=bgc_interp.isel(dep=slice(0,2))

# Match current coarsened data attributes
list_interp = list(bgc_interp.data_vars)
list_coarse = list(bgc_coarse.data_vars)

drop_list = list(set(list_interp)-set(list_coarse) - set(['temp_WOA','salt_WOA']))
bgc_interp = bgc_interp.drop_vars(drop_list)

# Save to netCDF to overwrite the old one 
bgc_interp.to_netcdf('./updated_files/coarsened_UNIFIED_bgc_dataset.nc')
