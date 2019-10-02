import logging
from collections import namedtuple

import numpy as np
from osgeo import gdal

LOGGER = logging.getLogger(__name__)
BandType = namedtuple("BandType", "gdal numpy")
INT32 = BandType(gdal.GDT_Int32, np.int32)
FLOAT64 = BandType(gdal.GDT_Float64, np.double)


def band_as_numpy(band, data_type=None):
    data_type = data_type if data_type else INT32
    scanline_buffer = band.ReadRaster(
        xoff=0, yoff=0, xsize=band.XSize, ysize=band.YSize,
        buf_xsize=band.XSize, buf_ysize=band.YSize, buf_type=data_type.gdal,
    )
    scanline = np.frombuffer(scanline_buffer, dtype=data_type.numpy)
    return np.reshape(scanline, (band.XSize, band.YSize))


def sub_band_as_numpy(band, y_limits, data_type=None):
    """Read subsets of the dataset so that we don't hold the whole thing
    in memory. It seems wasteful to reread parts, but GDAL keeps its own cache.
    """
    data_type = data_type if data_type else INT32
    y_size = y_limits[1] - y_limits[0]
    LOGGER.debug(f"sub_band y_size={y_size} y_limits {y_limits[0]}")
    scanline_buffer = band.ReadRaster(
        xoff=0,
        yoff=y_limits[0],
        xsize=band.XSize,
        ysize=y_size,
        buf_xsize=band.XSize,
        buf_ysize=y_size,
        buf_type=data_type.gdal,
    )
    scanline = np.frombuffer(scanline_buffer, dtype=data_type.numpy)
    return np.reshape(scanline, (band.XSize, y_size))
