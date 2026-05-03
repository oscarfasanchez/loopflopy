import pytest

from loopflopy._optional import MissingOptionalDependency, optional_import


pytestmark = pytest.mark.unit


def test_missing_optional_dependency_raises_clear_error_when_used():
    dependency = optional_import(
        "definitely_missing_loopflopy_dependency",
        install_hint="Install the missing package.",
    )

    assert isinstance(dependency, MissingOptionalDependency)
    with pytest.raises(ModuleNotFoundError, match="Install the missing package"):
        dependency.some_attribute
