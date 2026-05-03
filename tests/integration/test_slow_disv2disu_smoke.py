import numpy as np
import pytest

from loopflopy.disv2disu import Disv2Disu


pytestmark = [pytest.mark.integration, pytest.mark.slow]


def _structured_vertex_grid(ncol, nrow):
    vertices = []
    vertex_id = 0
    for row in range(nrow + 1):
        y = float(nrow - row)
        for col in range(ncol + 1):
            vertices.append([vertex_id, float(col), y])
            vertex_id += 1

    cell2d = []
    cell_id = 0
    for row in range(nrow):
        for col in range(ncol):
            upper_left = row * (ncol + 1) + col
            upper_right = upper_left + 1
            lower_left = upper_left + ncol + 1
            lower_right = lower_left + 1
            cell2d.append(
                [
                    cell_id,
                    col + 0.5,
                    nrow - row - 0.5,
                    4,
                    upper_left,
                    upper_right,
                    lower_right,
                    lower_left,
                ]
            )
            cell_id += 1

    return vertices, cell2d


def test_disv2disu_smoke_on_larger_structured_grid():
    ncol, nrow, nlay = 8, 6, 3
    ncpl = ncol * nrow
    vertices, cell2d = _structured_vertex_grid(ncol, nrow)
    top = np.full(ncpl, 30.0)
    botm = np.vstack([np.full(ncpl, 20.0), np.full(ncpl, 10.0), np.full(ncpl, 0.0)])

    converter = Disv2Disu(vertices, cell2d, top, botm, staggered=False)
    gridprops = converter.get_gridprops_disu6()

    assert gridprops["nodes"] == nlay * ncpl
    assert gridprops["nja"] == int(np.sum(gridprops["iac"]))
    assert len(gridprops["ja"]) == gridprops["nja"]
    assert len(gridprops["cell2d"]) == nlay * ncpl
