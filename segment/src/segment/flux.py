import networkx as nx
import numpy as np
from osgeo import gdal
from scipy.spatial import cKDTree

from .raster_access import band_as_numpy
from .raster_transform import pixel_coord, pixels_range_near_point, distance


def sum_within_box(arr_np, bounds):
    return 3


def average_within_box(arr_np, bounds):
    return 0.2


def assign_pop_and_pfpr_to_points(cities, lspop, pfpr, radius):
    """
    Given city locations, make approximate assignments of population
    and pfpr to those cities.

    For population, add all the population within a distance r.
    For pfpr, multiply pfpr by the population within the distance r.

    Args:
        cities:
        lspop:
        pfpr:
        radius (float): Distance of influence for that city.

    Returns:
        np.array: With shape (cities, 4) for pop, pfpr, longitude, latitude.
    """
    lspop = band_as_numpy(lspop.band)
    pop_geo = lspop.dataset.GetGeoTransform()
    pfpr = band_as_numpy(pfpr.band)
    pfpr_geo = pfpr.dataset.GetGeoTransform()

    pop_pfpr = np.zeros((len(cities), 4), dtype=np.float)
    for idx, city_coordinate_in_pop_raster in enumerate(cities):
        long_lat = pixel_coord(city_coordinate_in_pop_raster, pop_geo)
        pop_corners = pixels_range_near_point(long_lat, radius, pop_geo)
        pop = sum_within_box(lspop, pop_corners)
        pfpr_corners = pixels_range_near_point(long_lat, radius, pfpr_geo)
        pfpr = average_within_box(pfpr, pfpr_corners)
        pop_pfpr[idx] = [pop, pfpr, long_lat[0], long_lat[1]]
    return pop_pfpr


def calculate_gravity_constant(cutoff, exponent, plaquette_size):
    plaquette_r = int(cutoff / plaquette_size)
    axis = np.arange(-plaquette_r, plaquette_r + 1)
    i, j = np.meshgrid(axis, axis)
    distance = np.sqrt(i**2 + j**2)
    to_remove = np.where(np.abs(distance) < 1e-7)[0]
    np.delete(distance, to_remove)
    return 1 / np.sum(np.power(distance, 1 / exponent))


def calculate_flows(pop_pfpr, cutoff, exponent):
    lspop_scale = 1000  # a kilometer
    k = calculate_gravity_constant(cutoff, exponent, lspop_scale)
    cities = nx.Graph()
    cities.add_nodes_from(
        zip(
            range(pop_pfpr.shape[0]),
            [dict(longlat=x) for x in pop_pfpr[2:4]]
        )
    )

    kdtree = cKDTree(data=pop_pfpr[:, 3:4])
    for city_idx in range(pop_pfpr.shape[0]):
        near = kdtree.query_ball_point(pop_pfpr[city_idx, 2:4], cutoff)
        for n in near:
            if n == city_idx:
                continue
            r_ij = distance(pop_pfpr[city_idx, 2:4], pop_pfpr[n, 2:4])
            pfpr_avg = 0.5 * (pop_pfpr[city_idx, 1] + pop_pfpr[n, 1])
            flux = pfpr_avg * pop_pfpr[city_idx, 0] * pop_pfpr[n, 0] * k / r_ij**exponent
            cities.add_edge(city_idx, n, capacity=flux)
    return cities


def create_city_flows(cities, lspop, pfpr, radius):
    assert cities.shape[1] == 3
    # First column is distance to another city.
    # Next two are x and y into the pop band.

    assert str(gdal.GetDataTypeName(lspop.band.DataType)) == "Int32"
    assert str(gdal.GetDataTypeName(pfpr.band.DataType)) == "Float64"

    pop_pfpr = assign_pop_and_pfpr_to_points(cities, lspop, pfpr, radius)
    gravity_cutoff = 200_000
    exponent = 2.0
    city_graph = calculate_flows(pop_pfpr, gravity_cutoff, exponent)

    return city_graph
