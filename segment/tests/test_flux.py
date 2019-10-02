from segment.flux import calculate_gravity_constant


def test_calculate_gravity_constant_happy():
    k = calculate_gravity_constant(200_000, 2.0, 1000)
    print(k)
    assert k < 1
