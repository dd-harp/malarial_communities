import logging

import gdal

LOGGER = logging.getLogger(__name__)


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
    return dataset, band
