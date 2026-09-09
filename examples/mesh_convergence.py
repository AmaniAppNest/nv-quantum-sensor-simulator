"""Check displacement convergence with mesh refinement."""

import numpy as np

from fem.mesh import create_mesh
from fem.elasticity import solve_cantilever


mesh_sizes = [
    (20, 4),
    (40, 8),
    (80, 16),
]

for nx, ny in mesh_sizes:
    mesh = create_mesh(nx=nx, ny=ny)
    displacement = solve_cantilever(mesh)

    maximum_displacement = np.abs(displacement).max()

    print(
        f"Mesh {nx}x{ny}: "
        f"maximum displacement = {maximum_displacement:.6e} m"
    )
