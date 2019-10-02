from segment import input_data, find_cities


def test_load_lspop():
    landscan_file = find_cities.parser().parse_args([]).lspop
    lspop_ds, lspop_band = input_data.load_lspop(landscan_file)
    assert hasattr(lspop_ds, "GetDriver")
    assert hasattr(lspop_band, "ReadRaster")
