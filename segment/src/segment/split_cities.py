"""
Reads a file with city peaks. Assigns a flow graph to it.
Partitions that flow graph into smaller parts.
"""
import csv
import logging
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime
from inspect import getfile, getmodule
from hashlib import sha256
from pathlib import Path
from secrets import token_hex

from osgeo import gdal

from .communities import split_graph, save_pandas
from .input_data import load_lspop, load_cities, load_pfpr
from .raster_transform import LongLat, pixel_corners_of_longlat_box
from .city_find import largest_within_distance

LOGGER = logging.getLogger(__name__)


def read_pfpr(pfpr_path):
    pass


def parser():
    here = Path(getfile(parser))
    base_path = here.parent.parent.parent.parent
    landscan_file = (base_path / "data"
                     / "LandScan Global 2017" / "lspop2017")
    pfpr_file = (base_path / "data" / "PfPR" / "Raster Data" /
                 "PfPR_median" / "PfPR_median_Global_admin0_2017.tif")
    output_path = Path("segmented.h5")
    parse_obj = ArgumentParser(
        description=getmodule(parser).__doc__,
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parse_obj.add_argument("--lspop", type=Path, default=landscan_file,
                           help=("Path to directory containing LandSat "
                                 "population raster"))
    parse_obj.add_argument("--peaks", type=Path, default="city_peaks.csv",
                           help=("Path to output csv file of peak radius, "
                                 "peak x, peak y."))
    parse_obj.add_argument("--pfpr", type=Path, default=pfpr_file,
                           help=("Path to PfPR data from MAP project."))
    parse_obj.add_argument("--segmented", type=Path, default=output_path,
                           help=("Path to output file"))
    parse_obj.add_argument("--verbose", "-v", action="count", help="verbose",
                           default=0)
    parse_obj.add_argument("--quiet", "-q", action="count", help="quiet",
                           default=0)
    return parse_obj


def entry():
    args = parser().parse_args()
    logging_level = logging.INFO - 10 * args.verbose + 10 * args.quiet
    logging.basicConfig(level=logging_level)

    gdal.AllRegister()  # Initializes drivers to read files.
    cities = load_cities(args.peaks)
    lspop = load_lspop(args.lspop)
    pfpr = load_pfpr(args.pfpr)

    city_graph_with_flows = create_city_flows(cities, lspop, pfpr)
    segmented, hierarchy = split_graph(city_graph_with_flows, 250)
    save_pandas(segmented, hierarchy, args.segmented)


if __name__ == "__main__":
    entry()
