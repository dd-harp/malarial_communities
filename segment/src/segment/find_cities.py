"""
A script that reads Landscan and produces a set of cities within a
specified bounding box of longitude and latitude.

Some longitudes and latitudes of interest:
Africa bounding box: Longitude -20, 55. Latitude -40, 40.

If you want to see which records.txt entry corresponds to a CSV,
run sha256sum on the file, and its hash will show up in records.txt.
The records.txt file is in TOML format.
"""
import csv
import logging
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime
from inspect import getfile, getmodule
from hashlib import sha256
from os import linesep
from pathlib import Path
from secrets import token_hex

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
    m = sha256(output_file.open("rb").read())
    return m.hexdigest()


def parser():
    here = Path(getfile(parser))
    landscan_file = (here.parent.parent.parent.parent / "data"
                     / "LandScan Global 2017" / "lspop2017")
    kampala = LongLat(0 + 18 / 60, 32 + 34 / 60)
    moroto = LongLat(2 + 31 / 60, 34 + 40 / 60)

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
    parse_obj.add_argument("--peak-radius", type=float, default=20,
                           help=("How many LandSat pixels around a peak must "
                                 "be less than that peak"))
    parse_obj.add_argument("--long", type=float, nargs="+",
                           default=[kampala.long, moroto.long],
                           help="Min and max longitude")
    parse_obj.add_argument("--lat", type=float, nargs="+",
                           default=[kampala.lat, moroto.lat],
                           help="Min and max latitude")
    return parse_obj


def write_args(out_path, args, additional):
    with out_path.open("a") as out:
        print(f"[{token_hex(8)}]", file=out)
        print(f"when={datetime.now()}", file=out)
        for arg in ["lspop", "peaks", "long", "lat"]:
            value = getattr(args, arg)
            print(f"{arg}={value}", file=out)
        print(f"peak-radius={args.peak_radius}", file=out)
        for k, v in additional.items():
            print(f"{k}={v}", file=out)
        print("", file=out)


def entry():
    args = parser().parse_args()
    logging.basicConfig(level=logging.DEBUG)

    assert args.peak_radius > 0
    if not args.peaks.parent.exists():
        LOGGER.error("Parent directory for output peaks csv doesn't exist.")
    assert args.lspop.exists()
    assert len(args.long) == 2, "Give a min and max longitude"
    assert len(args.lat) == 2, "Give a min and max latitude"

    gdal.AllRegister()  # Initializes drivers to read files.
    lspop_dataset, lspop_band = load_lspop(args.lspop)

    bounding_box = [LongLat(args.long[i], args.lat[i]) for i in [0, 1]]
    geo_transform = lspop_dataset.GetGeoTransform()
    uganda_pixel_range = pixel_corners_of_longlat_box(bounding_box, geo_transform)
    city_peaks = largest_within_distance(lspop_band, args.peak_radius, uganda_pixel_range)
    peaks_hash = write_peaks(city_peaks, args.peaks)
    write_args(Path("record.txt"), args, {"peaks-hash": peaks_hash})


if __name__ == "__main__":
    entry()
