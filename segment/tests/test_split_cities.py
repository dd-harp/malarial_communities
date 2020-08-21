from pathlib import Path

from segment.split_cities import parser


def test_split_cities_parser():
    """There is no city graph when not given"""
    p = parser().parse_args(["--peak-radius", "25"])
    assert p.city_graph is None


def test_split_cities_parser_give_graph():
    p = parser().parse_args(["--peak-radius", "25", "--city-graph", "z.pickle"])
    assert p.city_graph == Path("z.pickle")
