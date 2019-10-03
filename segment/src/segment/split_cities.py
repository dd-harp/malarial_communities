"""
Reads a file with city peaks. Assigns a flow graph to it.
Partitions that flow graph into smaller parts.
"""
import logging
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from inspect import getfile, getmodule
from pathlib import Path
from pickle import dump, load

from osgeo import gdal

from .communities import save_pandas, split_disconnected_graph
from .flux import create_city_flows
from .input_data import load_lspop, load_cities, load_pfpr

LOGGER = logging.getLogger(__name__)


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
    parse_obj.add_argument("--peak-radius", type=float, default=25,
                           help=("Distance in km for which peak is maximal."))
    parse_obj.add_argument("--largest-component", type=int, default=10,
                           help=("The largest number of cities that could "
                                 "be together in a single component."))
    parse_obj.add_argument("--city-graph", type=Path, default=None,
                           help=("A city graph pickle file."))
    parse_obj.add_argument("--verbose", "-v", action="count", help="verbose",
                           default=0)
    parse_obj.add_argument("--quiet", "-q", action="count", help="quiet",
                           default=0)
    return parse_obj


def entry():
    args = parser().parse_args()
    logging_level = logging.INFO - 10 * args.verbose + 10 * args.quiet
    logging.basicConfig(level=logging_level)

    make_city_graph = args.city_graph is None or not args.city_graph.exists()

    if make_city_graph:
        city_graph_with_flows = create_city_graph(args)
        if args.city_graph is not None:
            dump(city_graph_with_flows, args.city_graph.open("wb"))
    else:
        city_graph_with_flows = load(args.city_graph.open("rb"))

    graph, hierarchy = split_disconnected_graph(
        city_graph_with_flows,  args.largest_component
    )
    save_pandas(graph, hierarchy, args.segmented)


def create_city_graph(args):
    gdal.AllRegister()  # Initializes drivers to read files.
    for expand in ["peaks", "lspop", "pfpr"]:
        arg_path = getattr(args, expand).expanduser()
        if not arg_path.exists():
            LOGGER.error(f"Path to {expand} not found: {arg_path}")
            exit(1)
        setattr(args, expand, arg_path)
    cities = load_cities(args.peaks)
    lspop = load_lspop(args.lspop)
    pfpr = load_pfpr(args.pfpr)
    radius = args.peak_radius * 1000  # Convert to meters.
    city_graph_with_flows = create_city_flows(cities, lspop, pfpr, radius)
    return city_graph_with_flows


if __name__ == "__main__":
    entry()
