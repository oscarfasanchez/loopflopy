import pytest

from loopflopy.disv2disu import (
    ConnectionPropertyList,
    area_of_polygon,
    deg_anglex,
    distance,
    distance_normal,
)


pytestmark = pytest.mark.unit


def test_area_of_polygon_returns_signed_area():
    assert area_of_polygon([0, 1, 1, 0], [0, 0, 1, 1]) == pytest.approx(1.0)
    assert abs(area_of_polygon([0, 1, 1, 0], [0, 0, 1, 1])) == pytest.approx(1.0)


def test_distance_helpers():
    assert distance(0, 0, 3, 4) == pytest.approx(5.0)
    assert distance_normal(0, 0, 0, 1, 1, 1) == pytest.approx(1.0)


@pytest.mark.parametrize(
    ("start", "end", "expected"),
    [
        ((0, 0), (0, -1), 0.0),
        ((0, 0), (1, 0), 90.0),
        ((0, 0), (0, 1), 180.0),
        ((0, 0), (-1, 0), 270.0),
    ],
)
def test_deg_anglex_uses_modflow_angle_convention(start, end, expected):
    assert deg_anglex(start[0], start[1], end[0], end[1]) == pytest.approx(expected)


def test_connection_property_list_assigns_stable_incrementing_ids():
    connections = ConnectionPropertyList()

    first = connections.new_connection(connected_node=1, this_node=0, ihc=1, cl1=2, cl2=3, hwva=4, angldegx=90)
    second = connections.new_connection(connected_node=2, this_node=0, ihc=1, cl1=2, cl2=3, hwva=4, angldegx=180)

    assert first == 0
    assert second == 1
    assert connections.number_of_connections == 2
    assert connections.connection_dict[first].connected_node == 1
    assert connections.connection_dict[second].angldegx == 180
