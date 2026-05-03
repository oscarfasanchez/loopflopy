"""Helpers for optional runtime dependencies."""

from importlib import import_module


class MissingOptionalDependency:
    """Proxy that raises a clear error when a missing dependency is used."""

    def __init__(self, module_name, *, attr=None, install_hint=None, error=None):
        self.module_name = module_name
        self.attr = attr
        self.install_hint = install_hint
        self.error = error

    @property
    def display_name(self):
        if self.attr:
            return f"{self.module_name}.{self.attr}"
        return self.module_name

    def _raise(self):
        message = f"Dependency '{self.module_name}' is required for this operation."
        if self.install_hint:
            message = f"{message} {self.install_hint}"
        raise ModuleNotFoundError(message) from self.error

    def __getattr__(self, _name):
        self._raise()

    def __call__(self, *_args, **_kwargs):
        self._raise()

    def __repr__(self):
        return f"<missing optional dependency {self.display_name!r}>"


def optional_import(module_name, *, attr=None, install_hint=None):
    """Import a dependency, returning a lazy error proxy if it is unavailable."""

    try:
        module = import_module(module_name)
    except ModuleNotFoundError as error:
        return MissingOptionalDependency(
            module_name,
            attr=attr,
            install_hint=install_hint,
            error=error,
        )

    if attr is None:
        return module
    return getattr(module, attr)
