"""Strain-field extraction for the reduced-order diamond cantilever."""

import numpy as np
from skfem import Basis, ElementVector, ElementTriP1
from skfem.helpers import sym_grad

from fem.mesh import create_mesh
from fem.elasticity import solve_cantilever


def compute_strain(mesh, displacement):
    """Compute the symmetric strain tensor from the displacement field."""
    element = ElementVector(ElementTriP1())
    basis = Basis(mesh, element)

    displacement_field = basis.interpolate(displacement)
    strain = sym_grad(displacement_field)

    return strain


if __name__ == "__main__":
    mesh = create_mesh()
    displacement = solve_cantilever(mesh)
    strain = compute_strain(mesh, displacement)

    print(f"Strain shape: {strain.shape}")
    print(f"Maximum absolute strain: {np.abs(strain).max():.6e}")
