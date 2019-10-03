import logging
import shutil

import networkx as nx
from osgeo import gdal, ogr, osr

LOGGER = logging.getLogger(__name__)


def create_wgs84_spatial_reference():
    spatial_ref = osr.SpatialReference()
    spatial_ref.SetWellKnownGeogCS("WGS84")
    return spatial_ref


def write_points_file(graph, hierarchy, out_path):
    if out_path.exists():
        LOGGER.info(f"Deleting {out_path} to write another.")
        shutil.rmtree(out_path)
    driver_name = "ESRI Shapefile"
    driver = gdal.GetDriverByName(driver_name)
    dataset = driver.Create(
        str(out_path), 0, 0, 0, gdal.GDT_Unknown
    )
    layer = dataset.CreateLayer("cities", None, ogr.wkbPoint)
    if layer is None:
        raise RuntimeError(f"Could not create layer")

    group_defn = ogr.FieldDefn("group", ogr.OFTInteger)
    group_defn.SetWidth(1)
    layer.CreateField(group_defn)

    group_defn = ogr.FieldDefn("level", ogr.OFTInteger)
    group_defn.SetWidth(1)
    field = layer.CreateField(group_defn)

    for city in graph.nodes:
        group = graph.nodes[city]["group"]
        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetField("group", group)
        feature.SetField("level", len(nx.ancestors(hierarchy, group)))

        x, y = graph.nodes[city]["longlat"]
        point = ogr.Geometry(ogr.wkbPoint)
        point.SetPoint_2D(0, x, y)  # set the first point of the point.
        feature.SetGeometry(point)
        layer.CreateFeature(feature)
        feature.Destroy()

    dataset = None
