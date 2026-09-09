"""Finite-element mesh for the reduced-order diamond cantilever."""

import numpy as np
from skfem import MeshTri


def create_mesh(
    length=10e-6,
    height=2e-6,
    nx=40,
    ny=8,
):
    """Create a structured triangular mesh of the cantilever."""
    x = np.linspace(0.0, length, nx + 1)
    y = np.linspace(0.0, height, ny + 1)

    return MeshTri.init_tensor(x, y)
