"""Spatial representation of NV quantum sensors."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class NVSensor:
    """Represent the spatial configuration of a single NV sensor.

    Parameters
    ----------
    position:
        Cartesian position of the NV center in meters.
    orientation:
        NV axis as a three-component vector.
    """

    position: np.ndarray
    orientation: np.ndarray

    def __post_init__(self):
        position = np.asarray(self.position, dtype=float)
        orientation = np.asarray(self.orientation, dtype=float)

        if position.shape != (3,):
            raise ValueError("position must contain exactly three components.")

        if orientation.shape != (3,):
            raise ValueError("orientation must contain exactly three components.")

        norm = np.linalg.norm(orientation)

        if norm == 0.0:
            raise ValueError("orientation must be a non-zero vector.")

        object.__setattr__(self, "position", position)
        object.__setattr__(self, "orientation", orientation / norm)

    def distance_to(self, point):
        """Return the distance from the NV center to a Cartesian point."""
        point = np.asarray(point, dtype=float)

        if point.shape != (3,):
            raise ValueError("point must contain exactly three components.")

        return float(np.linalg.norm(self.position - point))