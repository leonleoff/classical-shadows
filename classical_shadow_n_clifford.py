import random

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import (
    Clifford,
    DensityMatrix,
    StabilizerState,
    random_clifford,
)

from abstract_cassical_shadow import AbstractClassicalShadow


# IMPORTANT: This implementation will store snapshots that are NOT passed through the inverse M map.
# this will be needed to be done when using the snapshots in some way.
class ClassicalShadow_N_CLIFFORD(AbstractClassicalShadow):

    def compute_snapshot(self, rotations, measurement):

        qc = QuantumCircuit(self.num_qubits)
        for i, bit in enumerate(measurement):
            if bit == 1:
                qc.x(i)  # apply X gate to flip |0> to |1>

        stab_state = StabilizerState(qc)

        u_dagger = rotations.adjoint()

        return stab_state.evolve(u_dagger)

    def get_random_rotations(self, num_qubits):
        # S. Bravyi and D. Maslov, Hadamard-free circuits expose the structure of the Clifford group. https://arxiv.org/abs/2003.09412
        return random_clifford(num_qubits)

    def make_rotated_state_ciruit(
        self,
        rotation_description: list[Clifford],
        state_creation_circuit: QuantumCircuit,
    ) -> QuantumCircuit:

        circuit = state_creation_circuit.copy()

        circuit.compose(rotation_description.to_circuit(), inplace=True)

        circuit.measure_all()
        return circuit

    def get_desity_matrix_from_snapshots(self):
        if not self.snapshots:
            raise ValueError("No snapshot present.")

        n = self.num_qubits

        sum_rho = np.zeros((2**n, 2**n), dtype=complex)

        identity = np.eye(2**n)

        scaling_factor = 2**n + 1

        for stab_state in self.snapshots:
            psi_matrix = stab_state.to_operator().data

            snapshot_rho = (scaling_factor * psi_matrix) - identity

            sum_rho += snapshot_rho

        return sum_rho / len(self.snapshots)
