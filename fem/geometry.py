"""Geometry definition for the reduced-order diamond mechanical model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CantileverGeometry:
    """Dimensions of a rectangular diamond cantilever."""

    length: float = 10e-6
    height: float = 2e-6


def create_geometry():
    """Return the geometry parameters for the diamond cantilever."""
    return CantileverGeometry()
