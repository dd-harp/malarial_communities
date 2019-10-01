"""
A script that reads Landscan and produces a set of cities within a
specified bounding box of longitude and latitude.
"""
import logging
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path

import gdal

from .input_data import load_lspop

LOGGER = logging.getLogger(__name__)


def parser():
    base_dir = Path.home() / "dev" / "malarial_communities"
    landscan_file = base_dir / "data" / "LandScan Global 2017" / "lspop2017"

    parse_obj = ArgumentParser(
        description=parser.__module__.__doc__,
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parse_obj.add_argument("--lspop", type=Path, default=landscan_file)
    return parse_obj


def entry():
    args = parser().parse_args()
    logging.basicConfig(level=logging.DEBUG)
    gdal.AllRegister()  # Initializes drivers to read files.


if __name__ == "__main__":
    entry()
