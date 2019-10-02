import logging
from collections import namedtuple

import numpy as np
from osgeo import gdal

LOGGER = logging.getLogger(__name__)


Raster = namedtuple("Raster", "dataset band")


def load_lspop(landscan_file):
    if not landscan_file.exists():
        LOGGER.error(f"The given file doesn't exist: {landscan_file}")
    dataset = gdal.Open(str(landscan_file), gdal.GA_ReadOnly)
    if not dataset:
        LOGGER.error(f"Could not open {landscan_file}.")

    band = dataset.GetRasterBand(1)
    # If these change, then check how the band is used later.
    assert str(gdal.GetDataTypeName(band.DataType)) == "Int32"
    projection = dataset.GetProjection()
    assert "WGS 84" in str(projection)
    return Raster(dataset, band)


def load_cities(peaks_path):
    """

    Args:
        peaks_path (Path): The city_peaks.csv file.

    Returns:
        Numpy list of peaks.
    """
    floats = np.loadtxt(str(peaks_path), skiprows=1, delimiter=",")
    return floats.astype(np.int32)


def load_pfpr(pfpr_file):
    """

    Args:
        pfpr_file (Path):

    Returns:
        A dataset and band that is Float64.
    """
    if not pfpr_file.exists():
        LOGGER.error(f"The given file doesn't exist: {pfpr_file}")
    dataset = gdal.Open(str(pfpr_file), gdal.GA_ReadOnly)
    if not dataset:
        LOGGER.error(f"Could not open {pfpr_file}.")

    band = dataset.GetRasterBand(1)
    # If these change, then check how the band is used later.
    data_type = str(gdal.GetDataTypeName(band.DataType))
    if data_type != "Float64":
        raise RuntimeError(f"Data type for pfpr is {data_type}")
    projection = dataset.GetProjection()
    assert "WGS 84" in str(projection)
    return Raster(dataset, band)
