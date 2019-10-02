from pathlib import Path

import pytest

from segment import find_cities


@pytest.mark.parametrize("arglist,result", [
    (["--lspop", "filename"], dict(lspop=Path("filename"))),
     (["--long", "3.4", "2.9"], dict(long=[3.4, 2.9])),
])
def test_parser_happy(arglist, result):
    args = find_cities.parser().parse_args(arglist)
    print(args)
    for k, v in result.items():
        assert getattr(args, k) == v
