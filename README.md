This a python project aimed on addressing maximizing satelite data. This is by the use of Google Earth engine python API known as geemap.

1):Thus,To use geemap, you must first sign up for a Google Earth Engine account.

2):Then create a python virtual env:
   conda create -n gee python=3.10
   gee is the name of virtual env you can use any other name
Make sure you have python install and miniconda or anaconda installed.

3): After creating the virtual env activate the virtual env:
    conda activate gee

4): Then for an easy and faster way to install  geemap is by the use of Mamba library. 
so, yo have to install Mamba library.
   conda install -n base mamba -c conda-forge
   
5): Then finally, will install the the geospatial libraries that are commonly used using a single command line known as "geospatial"
    mamba install -c conda-forge geospatial
The geospatial package only helps you install commonly used packages for geospatial analysis and data visualization with only one command, making it easier to set up a conda environment for geospatial analysis and avoid dependency conflicts during installation. The geospatial package itself does not have any meaningful functions yet. After installation, you can continue to the commonly used geospatial packages as usual.

6): Extra will install a pymongo lib 
This is basically will help in data retrival from mongoDB.

 
