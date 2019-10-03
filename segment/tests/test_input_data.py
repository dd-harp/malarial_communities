from segment import input_data, find_cities, split_cities


def test_load_lspop():
    landscan_file = find_cities.parser().parse_args([]).lspop
    lspop_ds, lspop_band = input_data.load_lspop(landscan_file)
    assert hasattr(lspop_ds, "GetDriver")
    assert hasattr(lspop_band, "ReadRaster")
    print(f"lspops geotransform {lspop_ds.GetGeoTransform()}")


def test_load_cities(tmp_path):
    f = tmp_path / "cities.csv"
    with f.open("w") as out:
        print("column stuff blah", file=out)
        print("243,42,307", file=out)
        print("333,1,17", file=out)

    result = input_data.load_cities(f)
    assert result.shape == (2, 3)
    assert result[0, 1] == 42
    assert result[1, 2] == 17


def test_load_pfpr():
    pfpr_file = split_cities.parser().parse_args([]).pfpr
    lspop_ds, lspop_band = input_data.load_pfpr(pfpr_file)
    assert hasattr(lspop_ds, "GetDriver")
    assert hasattr(lspop_band, "ReadRaster")
    print(f"pfpr geotransform {lspop_ds.GetGeoTransform()}")
