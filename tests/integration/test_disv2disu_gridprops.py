import numpy as np
import pytest

from loopflopy.disv2disu import Disv2Disu


pytestmark = pytest.mark.integration


def _two_cell_two_layer_grid():
    vertices = [
        [0, 0.0, 1.0],
        [1, 1.0, 1.0],
        [2, 2.0, 1.0],
        [3, 0.0, 0.0],
        [4, 1.0, 0.0],
        [5, 2.0, 0.0],
    ]
    cell2d = [
        [0, 0.5, 0.5, 4, 0, 1, 4, 3],
        [1, 1.5, 0.5, 4, 1, 2, 5, 4],
    ]
    top = np.array([10.0, 10.0])
    botm = np.array(
        [
            [5.0, 5.0],
            [0.0, 0.0],
        ]
    )
    return vertices, cell2d, top, botm


def test_disv2disu_builds_consistent_gridprops_for_small_layered_grid():
    vertices, cell2d, top, botm = _two_cell_two_layer_grid()

    converter = Disv2Disu(vertices, cell2d, top, botm, staggered=False)
    gridprops = converter.get_gridprops_disu6()

    assert gridprops["nodes"] == 4
    assert gridprops["nja"] == int(np.sum(gridprops["iac"]))
    assert len(gridprops["top"]) == gridprops["nodes"]
    assert len(gridprops["bot"]) == gridprops["nodes"]
    assert len(gridprops["area"]) == gridprops["nodes"]
    assert len(gridprops["cell2d"]) == gridprops["nodes"]
    assert set(gridprops["ihc"]) >= {0, 1}
    np.testing.assert_allclose(gridprops["area"], np.ones(4))


def test_disv2disu_respects_inactive_disv_cells():
    vertices, cell2d, top, botm = _two_cell_two_layer_grid()
    disv_idomain = np.array(
        [
            [1, 1],
            [1, 0],
        ]
    )

    converter = Disv2Disu(vertices, cell2d, top, botm, staggered=False, disv_idomain=disv_idomain)
    gridprops = converter.get_gridprops_disu6()

    assert gridprops["nodes"] == 3
    assert len(gridprops["cell2d"]) == 3
    assert np.all(converter.cellid[disv_idomain < 1] == -999)
