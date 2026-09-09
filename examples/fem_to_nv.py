"""Connect the FEM strain field to the NV Hamiltonian."""

import numpy as np

from fem.mesh import create_mesh
from fem.elasticity import solve_cantilever
from fem.strain_field import compute_strain
from nv.hamiltonian import nv_hamiltonian
from nv.strain_coupling import transverse_strain


mesh = create_mesh()
displacement = solve_cantilever(mesh)
strain = compute_strain(mesh, displacement)

strain_tensor = np.moveaxis(strain, (0, 1), (-2, -1))

effective_strain = transverse_strain(
    strain_tensor,
    coupling_hz_per_strain=1.0e12,
)

representative_strain = float(np.mean(effective_strain))

hamiltonian_without_strain = nv_hamiltonian(
    magnetic_field=[0.0, 0.0, 0.0],
)

hamiltonian_with_strain = nv_hamiltonian(
    magnetic_field=[0.0, 0.0, 0.0],
    strain=representative_strain,
)

energies_without_strain = np.sort(
    hamiltonian_without_strain.eigenenergies()
)

energies_with_strain = np.sort(
    hamiltonian_with_strain.eigenenergies()
)

print(f"Representative strain parameter: {representative_strain:.6e} Hz")
print("Energies without strain (Hz):")
print(energies_without_strain)

print("Energies with strain (Hz):")
print(energies_with_strain)