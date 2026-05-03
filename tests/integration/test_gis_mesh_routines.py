import pytest


pytestmark = [pytest.mark.integration, pytest.mark.gis]


def test_resample_shapely_polygon_preserves_polygon_type_and_bounds():
    pytest.importorskip("shapely")
    pytest.importorskip("geopandas")
    pytest.importorskip("flopy")

    from shapely.geometry import Polygon

    from loopflopy.mesh_routines import resample_shapely_poly

    polygon = Polygon([(0.0, 0.0), (4.0, 0.0), (4.0, 2.0), (0.0, 2.0), (0.0, 0.0)])

    result = resample_shapely_poly(polygon, distance=1.0)

    assert result.geom_type == "Polygon"
    assert result.bounds == pytest.approx(polygon.bounds)
    assert result.area == pytest.approx(polygon.area)
