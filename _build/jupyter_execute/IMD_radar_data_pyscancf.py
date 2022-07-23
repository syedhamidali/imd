#!/usr/bin/env python
# coding: utf-8

# ## How to handle IMD radar data efficiently?

#     1. Make sure you have anaconda or miniconda installed or install it using any link given below;
#     https://docs.conda.io/en/latest/miniconda.html
#     https://www.anaconda.com/products/individual
#     
#     2. Install the required libraries/packages listed below;
#     required: notebook, pyart, xarray, dask, pyscancf, git
#     optional: wradlib
#     
#     How to install these packages?
#     1. Open conda command propmt or terminal after installing anaconda/miniconda
#     2. type the following command
#         conda install -c conda-forge xarray arm_pyart dask git notebook wradlib 
#     For pyscancf, please use: 
#         pip install git+https://github.com/syedhamidali/PyScanCf.git 
#     Please cite if you use pyscancf 
#     H.A. Syed, I. Sayyed, M.C.R. Kalapureddy, & K.K. Grandhi. (2021). 
#     PyScanCf – The library for single sweep datasets of IMD weather radars.
#     Zenodo. https://doi.org/10.5281/zenodo.5574160

# ### Let's import these installed libraries,

# In[1]:


import xarray as xr
import numpy as np


# In[2]:


import glob #used to load the data using glob into this notebook


# In[3]:


files = sorted(glob.glob("../MUM200829IMD/*"))


# #### We are interested in 250 km range radar scans i.e short range ppi, so we will select the files having 500 km range and move them into another directory

# So first I created an empty list "file500" in which I appended the file names of 500 km range scans

# In[4]:


file500 = []
for file in files:
    ds = xr.open_dataset(file)
    if ds.unambigRange > 300:
        print(file, " : ", len(ds.radial.values),len(ds.bin.values),ds.unambigRange.values)
        file500.append(file)


# In[5]:


pwd


# In[6]:


import os
import shutil


# In[7]:


os.mkdir('/Users/rizvi/Downloads/IMD500')


# In[63]:


fmv = []
for file in file500:
#     print(file.split("/")[-1])
    fmv.append(file.split("/")[-1])


# In[64]:


fmv


# In[65]:


import shutil

source_folder = r"../MUM200829IMD/"
destination_folder = r"../IMD500/"
files_to_move = fmv

# iterate files
for file in files_to_move:
    # construct full file path
    source = source_folder + file
    destination = destination_folder + file
    # move file
    shutil.move(source, destination)
    print('Moved:', file)


# In[ ]:





# ### Now we have only short range ppis in the "MUM200829IMD" directory and we will convert these files to cfradial files by using pyscancf

# In[66]:


import pyscancf.pyscancf as pcf


# In[67]:


pcf.cfrad("../MUM200829IMD/",output_dir='../akki/',)


# ### Now that cfradial files are being created, we shall convert those files further to gridded datasets

# In[68]:


import pyart


# In[71]:


cf_files = sorted(glob.glob("pol*nc")) # loading cfradial data


# In[183]:


# creating directory for gridded files, which we are going to create by converting cfradial or polar data
os.mkdir("/Users/rizvi/Downloads/outgrid")


# In[184]:


output_grid_folder = "/Users/rizvi/Downloads/outgrid/"


# In[205]:


for file in cf_files[0:10]:
    radar = pyart.io.read_cfradial(file)
    grid = pyart.map.grid_from_radars(radar,(10,400,400),
                   ((0.,5000.),(-248000.,248000.),(-248000.,248000.)), 
                                   weighting_function='Barnes2',
                                  fields=['REF'],)
    pyart.io.write_grid(output_grid_folder+"grid_"+file.split("_")[-1],grid=grid)


# In[ ]:





# In[ ]:





# ### test output grid files

# In[206]:


rad_ds = xr.open_mfdataset(output_grid_folder+"/*")


# In[207]:


rad_ds['REF'].where(rad_ds.REF<100).mean("time").isel(z=2).plot()


# In[211]:


rad_ds['REF'].where(rad_ds.REF<100).mean(["x","y"]).isel(z=2).plot()


# In[ ]:




