import numpy as np

from fem.mesh import create_mesh
from fem.elasticity import solve_cantilever
from fem.strain_field import compute_strain


def test_mesh_has_expected_structure():
    mesh = create_mesh(
        nx=20,
        ny=4,
    )

    assert mesh.p.shape[0] == 2
    assert mesh.t.shape[0] == 3
    assert mesh.p.shape[1] > 0
    assert mesh.t.shape[1] > 0


def test_cantilever_has_nonzero_displacement():
    mesh = create_mesh(
        nx=20,
        ny=4,
    )

    displacement = solve_cantilever(mesh)

    assert displacement.shape[0] == 2 * mesh.p.shape[1]
    assert np.max(np.abs(displacement)) > 0.0


def test_strain_field_is_finite():
    mesh = create_mesh(
        nx=20,
        ny=4,
    )

    displacement = solve_cantilever(mesh)
    strain = compute_strain(mesh, displacement)

    assert strain.shape[0:2] == (2, 2)
    assert np.all(np.isfinite(strain)) 