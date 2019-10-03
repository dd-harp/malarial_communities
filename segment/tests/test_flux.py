import numpy as np

from segment.flux import calculate_gravity_constant, sum_within_box


def test_calculate_gravity_constant_happy():
    k = calculate_gravity_constant(200_000, 2.0, 1000)
    print(f"The gravity constant is {k}")
    assert k > 0
    assert k < 1e-3


def test_sum_within_box_out_of_bounds():
    """Sum ignores values outside bounds."""
    a = np.array([[0, 1, 3], [-99999, 2, -99999]], dtype=np.float)
    total = sum_within_box(a, [[0, 4], [0, 4]])
    assert total == 6
