from pathlib import Path
from segment import input_data


def test_load_lspop():
    base_dir = Path.home() / "dev" / "malarial_communities"
    landscan_file = base_dir / "data" / "LandScan Global 2017" / "lspop2017"
    lspop = input_data.load_lspop(landscan_file)
