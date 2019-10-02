import logging
from itertools import product
from os import linesep

from progressbar import progressbar

from .raster_access import sub_band_as_numpy
from .raster_transform import LongLat

LOGGER = logging.getLogger(__name__)


def largest_within_distance(band, distance, bounding_box_pixels=None):
    """
    Find the largest pixel within the given distance.
    """
    dx2 = distance**2
    value_range = (int(band.GetMinimum()), int(band.GetMaximum()))
    maximum_distance = max(band.XSize, band.YSize)**2
    peaks = list()
    not_a_peak = 0
    if not bounding_box_pixels:
        bounding_box_pixels = LongLat([0, band.XSize], [0, band.YSize])
    for j in progressbar(range(*bounding_box_pixels.lat)):
        y_limits = (int(max(0, j - distance)),
                    int(min(band.YSize, j + distance + 1)))
        map_j = j - y_limits[0]
        map = sub_band_as_numpy(band, y_limits)
        for i in range(*bounding_box_pixels.long):
            if map[i, map_j] < value_range[0] + 1:
                continue
            x_limits = (int(max(0, i - distance)),
                        int(min(band.XSize, i + distance + 1)))
            minimum_distance = maximum_distance
            for (x, y) in product(range(*x_limits), range(map.shape[1])):
                if map[x, y] > map[i, map_j]:
                    minimum_distance = min(minimum_distance, (x - i)**2 + (y - map_j)**2)
            if minimum_distance > dx2 and minimum_distance < maximum_distance:
                peaks.append((minimum_distance, i, j))
            else:
                not_a_peak += 1
    print(f"{linesep}Found {len(peaks)} and discarded {not_a_peak}.")
    peaks.sort()
    return peaks
