"""
A script that reads Landscan and produces a set of cities within a
specified bounding box of longitude and latitude.
"""
import csv
import logging
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from inspect import getfile
from pathlib import Path

from osgeo import gdal

from .input_data import load_lspop
from .raster_transform import LongLat, pixel_corners_of_longlat_box
from .city_find import largest_within_distance

LOGGER = logging.getLogger(__name__)


def write_peaks(city_peaks, output_file):
    with output_file.open("w") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["squared distance", "x", "y"])
        for dx, x, y in city_peaks:
            writer.writerow([str(dx), str(x), str(y)])


def parser():
    here = Path(getfile(parser))
    landscan_file = (here.parent.parent.parent.parent / "data"
                     / "LandScan Global 2017" / "lspop2017")

    parse_obj = ArgumentParser(
        description=parser.__module__.__doc__,
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parse_obj.add_argument("--lspop", type=Path, default=landscan_file)
    parse_obj.add_argument("--peaks", type=Path, default="city_peaks.csv")
    return parse_obj


def entry():
    args = parser().parse_args()
    logging.basicConfig(level=logging.DEBUG)
    gdal.AllRegister()  # Initializes drivers to read files.
    lspop_dataset, lspop_band = load_lspop(args.lspop)

    # africa_corners = [LongLat(-20, -40), LongLat(55, 40)]
    kampala = LongLat(0 + 18 / 60, 32 + 34 / 60)
    moroto = LongLat(2 + 31 / 60, 34 + 40 / 60)
    geo_transform = lspop_dataset.GetGeoTransform()
    uganda_pixel_range = pixel_corners_of_longlat_box([kampala, moroto], geo_transform)
    city_peaks = largest_within_distance(lspop_band, 20, uganda_pixel_range)
    write_peaks(city_peaks, args.peaks)


if __name__ == "__main__":
    entry()
