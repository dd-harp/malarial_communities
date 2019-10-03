import numpy as np
import pytest


from segment.raster_transform import (
    pixels_range_near_point, pixel_coord, pixel_containing,
    long_lat_to_xyz,
)


@pytest.fixture
def lspop_geo():
    return (-180.0, 0.0083333333333333, 0.0, 89.99999999999929,
            0.0, -0.0083333333333333)


@pytest.fixture
def pfpr_geo():
    return -118.375, 0.04166665, 0.0, 53.541623217, 0.0, -0.04166665


def test_coord_containing(lspop_geo):
    pixel = [25199.5, 10768.5]
    coord = pixel_coord(pixel, lspop_geo)
    assert 10 < coord[0] < 50
    assert -10 < coord[1] < 10
    containing = pixel_containing(coord, lspop_geo)
    assert containing[0] == 25199
    assert containing[1] == 10768


def test_pixels_range_near_point_lspop(lspop_geo):
    long_lat = [30, 1]
    minmax = pixels_range_near_point(long_lat, 100_000, lspop_geo)
    print(f"pixels minmax {minmax}")
    assert minmax.long[1] > minmax.long[0]
    assert minmax.lat[1] > minmax.lat[0]

    center_ish = [0.5 * (minmax.long[0] + minmax.long[1]),
                  0.5 * (minmax.lat[0] + minmax.lat[1])]
    coord = pixel_coord(center_ish, lspop_geo)
    print(f"pixel center {coord}")


def test_pixels_range_near_point_pfpr(pfpr_geo):
    long_lat = [30, 1]
    minmax = pixels_range_near_point(long_lat, 100_000, pfpr_geo)
    print(f"pixels minmax {minmax}")
    for i in [0, 1]:
        for j in [0, 1]:
            assert minmax[i][j] > 0

    center_ish = [0.5 * (minmax.long[0] + minmax.long[1]),
                  0.5 * (minmax.lat[0] + minmax.lat[1])]
    coord = pixel_coord(center_ish, pfpr_geo)
    print(f"pixel center {coord}")


def test_long_lat_to_xyz():
    ll = np.array([
        [30, 0],
        [30, 1],
        [28, 0],
        [22, 0],
    ], dtype=np.float)
    ans = long_lat_to_xyz(ll)
    assert ans.shape == (4, 3)
    print(ans)