Install
=======

I got this working in a Conda environment because Conda could provide
GDAL 3.0, while GDAL 2.4 was the default installation for my OS.

For Ubuntu, if you have the latest OS version, the GDAL ppa isn't
updated for the latest OS, so it won't run. The best bet is to use
a slightly-older Ubuntu and find the ubuntugis ppa.

 1. conda create -n venv numpy scipy
 2. conda install gdal poppler kealib pytables
 3. conda install matplotlib
 4. pip install -e segment
