from types import SimpleNamespace

import numpy as np
import pytest

from loopflopy import utils


pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("k", "j", "i", "expected"),
    [
        (0, 0, 0, 0),
        (0, 0, 3, 3),
        (0, 1, 0, 4),
        (1, 0, 0, 12),
        (2, 2, 3, 35),
    ],
)
def test_find_cellid_uses_zero_based_layer_row_column_order(k, j, i, expected):
    assert utils.find_cellid(k, j, i, nlay=3, nrow=3, ncol=4) == expected


def test_find_kji_round_trips_zero_based_cell_ids():
    nlay, nrow, ncol = 3, 3, 4

    for k in range(nlay):
        for j in range(nrow):
            for i in range(ncol):
                cellid = utils.find_cellid(k, j, i, nlay, nrow, ncol)
                assert utils.find_kji(cellid, nlay, nrow, ncol) == (k, j, i)


def test_structured_coordinate_helpers():
    assert utils.x_to_col(19.9, delr=10) == 1
    assert utils.y_to_row(20.1, delc=10) == 2
    assert utils.z_to_lay(75.0, delz=10.0, zmax=100.0) == 2
    assert utils.xyz_to_discell(x=25, y=75, x0=0, y1=100, dx=10, dy=10) == (2, 2, (25.0, 75.0))


def test_lay_to_z_returns_layer_midpoint():
    botm = np.array([[90.0, 80.0], [70.0, 60.0]])
    top = np.array([100.0, 90.0])

    assert utils.lay_to_z(botm, top, lay=0, icpl=0) == pytest.approx(95.0)
    assert utils.lay_to_z(botm, top, lay=1, icpl=0) == pytest.approx(80.0)


def test_disv_disu_cell_mapping_helpers():
    geomodel = SimpleNamespace(
        cellid_disv=np.arange(6).reshape(2, 3),
        cellid_disu=np.array([[0, 1, -1], [2, 3, 4]]),
    )

    assert utils.disvcell_to_disucell(geomodel, 4) == 3
    assert utils.disucell_to_disvcell(geomodel, 3) == 4
    assert utils.disvcell_to_layicpl(geomodel, 4) == (1, 1)
    assert utils.disucell_to_layicpl(geomodel, 3) == (1, 1)


def test_ch_flow_splits_negative_and_positive_boundary_flow():
    assert utils.ch_flow([(0, 0, -2.5), (0, 1, 0.5), (0, 2, 1.5)]) == (-2.5, 2.0)
