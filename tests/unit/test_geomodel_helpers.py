import numpy as np
import pytest

from loopflopy.geomodel import (
    find_angle1,
    find_angle1_transect,
    find_angle2,
    find_angle2_transect,
    reshape_loop2mf,
)


pytestmark = pytest.mark.unit


def test_reshape_loop2mf_flips_loop_layer_order_to_modflow_order():
    values = np.arange(6)

    result = reshape_loop2mf(values, nlay=3, ncpl=2)

    np.testing.assert_array_equal(result, np.array([[4, 5], [2, 3], [0, 1]]))


@pytest.mark.parametrize(
    ("normal_vector", "expected_angle1", "expected_angle2"),
    [
        (np.array([0.0, 0.0, 1.0]), 0.0, 0.0),
        (np.array([1.0, 0.0, 1.0]), 180.0, 45.0),
        (np.array([0.0, 1.0, 1.0]), 90.0, 45.0),
    ],
)
def test_find_angles_from_surface_normal(normal_vector, expected_angle1, expected_angle2):
    assert find_angle1(normal_vector) == pytest.approx(expected_angle1)
    assert find_angle2(normal_vector) == pytest.approx(expected_angle2)


def test_transect_angle1_uses_rotation_angle():
    assert find_angle1_transect(np.array([0.0, 1.0, 1.0]), rotation_angle=37.5) == 37.5


def test_transect_angle2_uses_normal_vector_and_rotation_angle():
    angle = find_angle2_transect(np.array([0.0, 0.0, 1.0]), rotation_angle=0.0)

    assert angle == pytest.approx(0.0)
