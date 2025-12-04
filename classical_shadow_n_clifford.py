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

    def compute_clifford_applied_to_measurements(
        self, rotations, measurement
    ) -> list[StabilizerState]:

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

    def get_desity_matrix_from_stabilizers(self):
        if not self.stabilizer_list_list:
            raise ValueError("No snapshot present.")

        n = self.num_qubits

        sum_rho = np.zeros((2**n, 2**n), dtype=complex)

        identity = np.eye(2**n)

        scaling_factor = 2**n + 1

        for stab_state in self.stabilizer_list_list:
            psi_matrix = stab_state.to_operator().data

            snapshot_rho = (scaling_factor * psi_matrix) - identity

            sum_rho += snapshot_rho

        return sum_rho / len(self.stabilizer_list_list)

    def make_rotated_state_circuit(
        self, cliffords: list[Clifford], state_creation_circuit: QuantumCircuit
    ) -> QuantumCircuit:
        assert len(cliffords) == 1
        clifford = cliffords[0]
        assert clifford.num_qubits == state_creation_circuit.num_qubits

        combined_circuit = state_creation_circuit.copy()
        combined_circuit.remove_final_measurements()

        # apply the gloabal clifford
        clifford_circuit: QuantumCircuit = clifford.to_circuit()
        combined_circuit.compose(clifford_circuit, inplace=True)
        combined_circuit.measure_all()

        return combined_circuit
