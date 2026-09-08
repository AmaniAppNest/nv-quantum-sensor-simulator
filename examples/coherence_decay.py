import numpy as np
import qutip as qt
import matplotlib.pyplot as plt

from nv.hamiltonian import nv_hamiltonian
from nv.lindblad import evolve_density_matrix, coherence


hamiltonian = nv_hamiltonian([0.0, 0.0, 0.0])

ms_zero = qt.basis(3, 1)
ms_plus = qt.basis(3, 0)
initial_state = (ms_zero + ms_plus).unit()

times = np.linspace(0.0, 2e-6, 101)

result = evolve_density_matrix(
    hamiltonian,
    initial_state,
    times,
    dephasing_rate=1.0e6,
)

coherence_values = [
    coherence(state)
    for state in result.states
]

plt.figure()
plt.plot(times * 1e6, coherence_values)
plt.xlabel("Time (µs)")
plt.ylabel("Coherence")
plt.title("NV coherence decay under Lindblad dephasing")
plt.tight_layout()
plt.savefig("results/coherence_decay.png", dpi=200)
plt.show()
