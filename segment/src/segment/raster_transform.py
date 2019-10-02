from collections import namedtuple
from math import floor


LongLat = namedtuple("LongLat", "long lat")
"""Longitude and latitude always get reversed, so use this to help."""


def pixel_containing(point, geo_transform):
    """
    Which pixel has this long-lat?

    Args:
        point: A point in longitude and latitude.
        geo_transform: Six points for a transformation with shear.

    Returns:
        List[int]: Wiht an x, y of the containing point.
    """
    return [
        int(floor(1.0 / geo_transform[1]) * (point[0] - geo_transform[0])),
        int(floor(1.0 / geo_transform[5]) * (point[1] - geo_transform[3])),
    ]


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
