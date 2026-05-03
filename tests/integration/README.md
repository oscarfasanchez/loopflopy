# Integration Tests

This folder contains non-default tests for behavior that is broader or heavier
than fast unit checks. Some tests run with core dependencies only; others use
`pytest.importorskip` so they are collected but skipped when optional GIS/modeling
dependencies are not installed.

Mark those tests with `@pytest.mark.integration` plus any relevant marker such as
`@pytest.mark.gis` or `@pytest.mark.slow` so they stay out of the default fast
local test run.
