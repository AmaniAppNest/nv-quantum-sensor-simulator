
"""Generic multiphysics field-data representation."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class FieldData:
    """Represent a spatially sampled physical field."""

    positions: np.ndarray
    values: np.ndarray
    name: str = "field"
    units: str = ""

    def __post_init__(self):
        positions = np.asarray(self.positions, dtype=float)
        values = np.asarray(self.values, dtype=float)

        if positions.ndim != 2 or positions.shape[1] != 3:
            raise ValueError("positions must have shape (N, 3).")

        if values.shape[0] != positions.shape[0]:
            raise ValueError(
                "values must contain one entry for each position."
            )

        if positions.shape[0] == 0:
            raise ValueError("field data must contain at least one position.")

        object.__setattr__(self, "positions", positions)
        object.__setattr__(self, "values", values)

    @property
    def n_points(self):
        """Return the number of spatial samples."""
        return self.positions.shape[0]

    def nearest_value(self, point):
        """Return the field value at the nearest sampled position."""
        point = np.asarray(point, dtype=float)

        if point.shape != (3,):
            raise ValueError("point must contain exactly three components.")

        distances = np.linalg.norm(self.positions - point, axis=1)
        index = np.argmin(distances)

        return self.values[index]
