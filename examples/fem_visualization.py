"""Visualize displacement and strain from the diamond cantilever FEM model."""

import numpy as np
import matplotlib.pyplot as plt

from fem.mesh import create_mesh
from fem.elasticity import solve_cantilever
from fem.strain_field import compute_strain


mesh = create_mesh()
displacement = solve_cantilever(mesh)
strain = compute_strain(mesh, displacement)

ux = displacement[0::2]
uy = displacement[1::2]

displacement_magnitude = np.sqrt(ux**2 + uy**2)

strain_xx = np.mean(strain[0, 0], axis=1)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

mesh.draw(
    ax=axes[0],
    color=displacement_magnitude,
)
axes[0].set_title("Displacement magnitude")
axes[0].set_xlabel("x (m)")
axes[0].set_ylabel("y (m)")

mesh.draw(
    ax=axes[1],
    color=strain_xx,
)
axes[1].set_title("Normal strain $\\epsilon_{xx}$")
axes[1].set_xlabel("x (m)")
axes[1].set_ylabel("y (m)")

plt.tight_layout()
plt.savefig("results/fem_fields.png", dpi=200)
plt.show()
