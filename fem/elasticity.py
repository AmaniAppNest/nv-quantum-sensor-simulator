"""Linear elasticity solver for the diamond cantilever."""

import numpy as np

from skfem import (
    Basis,
    FacetBasis,
    ElementVector,
    ElementTriP1,
    LinearForm,
    BilinearForm,
)
from skfem import asm, condense, solve
from skfem.helpers import ddot, sym_grad, trace


def solve_cantilever(
    mesh,
    youngs_modulus=1.05e12,
    poisson_ratio=0.10,
):
    """Solve plane-stress elasticity for the diamond cantilever."""
    element = ElementVector(ElementTriP1())
    basis = Basis(mesh, element)

    mu = youngs_modulus / (2.0 * (1.0 + poisson_ratio))
    lam = (
        youngs_modulus
        * poisson_ratio
        / (1.0 - poisson_ratio**2)
    )

    @BilinearForm
    def bilinf(u, v, w):
        strain_u = sym_grad(u)
        strain_v = sym_grad(v)

        return (
            2.0 * mu * ddot(strain_u, strain_v)
            + lam * trace(strain_u) * trace(strain_v)
        )

    right_boundary = mesh.facets_satisfying(
        lambda x: np.isclose(x[0], mesh.p[0].max())
    )

    facet_basis = FacetBasis(
        mesh,
        element,
        facets=right_boundary,
    )

    @LinearForm
    def traction(v, w):
        return -1.0e6 * v[1]

    stiffness = asm(bilinf, basis)
    force = asm(traction, facet_basis)

    left_boundary = mesh.facets_satisfying(
        lambda x: np.isclose(x[0], 0.0)
    )

    dofs = basis.get_dofs(facets=left_boundary)

    system = condense(
        stiffness,
        force,
        D=dofs,
    )

    displacement = solve(
        system[0],
        system[1],
    )

    full_displacement = system[2].copy()
    full_displacement[system[3]] = displacement

    return full_displacement 
