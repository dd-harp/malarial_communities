from collections import namedtuple
from enum import Enum
from math import floor

import numpy as np
from geographiclib import geodesic

WGS84 = geodesic.Geodesic(
    geodesic.Constants.WGS84_a, geodesic.Constants.WGS84_f)
LongLat = namedtuple("LongLat", "long lat")
"""Longitude and latitude always get reversed, so use this to help."""


class Direction(Enum):
    North = 0
    East = 90
    South = 180
    West = 270


def pixel_containing(point, geo_transform):
    """
    Which pixel has this long-lat?

    Args:
        point: A point in longitude and latitude.
        geo_transform: Six points for a transformation with shear.

    Returns:
        List[int]: With an x, y of the containing point.
    """
    return [
        int(floor(1.0 / geo_transform[1]) * (point[0] - geo_transform[0])),
        int(floor(1.0 / geo_transform[5]) * (point[1] - geo_transform[3])),
    ]


def pixel_coord(point, geo_transform):
    """Return long-lat of point."""
    return [
        geo_transform[0] + point[0] * geo_transform[1] + point[1] * geo_transform[2],
        geo_transform[3] + point[0] * geo_transform[4] + point[1] * geo_transform[5],
    ]


def pixels_range_near_point(point, radius_in_meters, geo_transform):
    """

    Args:
        point (Tuple[float,float]): Longitude and latitude.
        radius_in_meters (float): Distance to search.
        geo_transform (WGS84 raster transform): Says per-pixel transform.

    Returns:
        Range of long-lats to search.
    """
    # lat, then long
    longlat = np.zeros((4, 2), dtype=np.int)
    for idx, direction in enumerate(Direction):
        geo_dict = WGS84.Direct(
            point[1], point[0], direction, radius_in_meters
        )
        far_point = [geo_dict["lon2"], geo_dict["lat2"]]
        longlat[idx] = pixel_containing(far_point, geo_transform)

    return LongLat([longlat[:, 0].min(), longlat[:, 0].max()],
                   [longlat[:, 1].min(), longlat[:, 1].max()])


def distance(a_longlat, b_longlat):
    geo_dict = WGS84.Inverse(
        a_longlat[1], a_longlat[0], b_longlat[1], b_longlat[0]
    )
    return geo_dict["s12"]


def pixel_corners_of_longlat_box(corners, geo_transform):
    """
    Find the (x,y) pixels in the raster for the long-lat corners given.

    Args:
        corners: Lowerleft and upper-right
        geo_transform: vector length 6 from GDAL.

    Returns:
        LongLat[List[int]]: A LongLat that contains a lower and upper longitude
                            and a lower and upper latitude.
    """
    longlat_corners = [
        [corners[a].long, corners[b].lat]
        for (a, b) in [[0, 0], [0, 1], [1, 0], [1, 1]]
    ]

    corner_pixels = [pixel_containing(corner, geo_transform) for corner in longlat_corners]
    longitude_range = [
        min([x[0] for x in corner_pixels]),
        max([x[0] for x in corner_pixels]),
    ]
    latitude_range = [
        min([x[1] for x in corner_pixels]),
        max([x[1] for x in corner_pixels]),
    ]
    # This is a pair of longitudes and a pair of latitudes.
    return LongLat(longitude_range, latitude_range)
