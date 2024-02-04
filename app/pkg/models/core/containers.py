from dataclasses import dataclass, field
from typing import Callable, List, Optional

from dependency_injector import containers
from fastapi import FastAPI

__all__ = ["Container", "Containers"]


@dataclass(frozen=True)
class Container:
    """Model for contain single container."""

    container: Callable[..., containers.Container]
    packages: List[str] = field(default_factory=lambda: ["app"])


@dataclass(frozen=True)
class Containers:
    """Frozen dataclass model, for contains all declarative containers."""

    #: str: __name__ of main package.
    pkg_name: str

    #: List[Container]: List of `Container` model.
    containers: List[Container]

    def wire_packages(
        self,
        app: Optional[FastAPI] = None,
        pkg_name: Optional[str] = None,
    ):
        """Wire packages to the declarative containers."""

        pkg_name = pkg_name if pkg_name else self.pkg_name
        print("pkg_name", pkg_name)

        for container in self.containers:
            cont = container.container()
            cont.wire(packages=[pkg_name, *container.packages])
            if app:
                setattr(app, container.container.__name__.lower(), cont)
