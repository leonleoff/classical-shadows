import random

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import (
    Clifford,
    DensityMatrix,
    StabilizerState,
    random_clifford,
)
from qiskit.visualization import array_to_latex

from abstract_cassical_shadow import AbstractClassicalShadow


class ClassicalShadow_N_CLIFFORD(AbstractClassicalShadow):

    def compute_clifford_applied_to_measurements(
        self, cliffords, measurement_results
    ) -> list[StabilizerState]:
        assert len(cliffords) == 1
        assert len(measurement_results) == self.num_qubits

        base_state_qc = QuantumCircuit(
            self.num_qubits
        )  # As this is a qiskit circuit the qbit order is here wrong

        for i, bit in enumerate(measurement_results):
            if bit == 1:
                base_state_qc.x(i)

        base_stab = StabilizerState(base_state_qc)
        state = base_stab.copy()

        pre_measurement_state: StabilizerState = state.evolve(cliffords[0].adjoint())

        # we need to change the qbit order here to ensure the mathmatical order of qbits
        qc_reverse = QuantumCircuit(self.num_qubits)
        for i in range(self.num_qubits // 2):
            qc_reverse.swap(i, self.num_qubits - 1 - i)
        clifford_reverse = Clifford(qc_reverse)
        reversed_state: StabilizerState = pre_measurement_state.evolve(clifford_reverse)

        return [reversed_state]

    def get_random_rotations(self, num_qubits):
        # S. Bravyi and D. Maslov, Hadamard-free circuits expose the structure of the Clifford group. https://arxiv.org/abs/2003.09412
        return [random_clifford(num_qubits)]

    def get_density_matrix_from_stabilizers(self):
        if not self.stabilizer_list_list:
            raise ValueError("No snapshot present.")

        sum_rho = None
        for i, row in enumerate(self.stabilizer_list_list):
            assert len(row) == 1
            dm_data: DensityMatrix = self.stabilizer_to_density_matrix(row[0])
            inverted_dm = ((2**self.num_qubits) + 1) * dm_data - np.eye(
                2**self.num_qubits
            )
            if sum_rho is None:
                sum_rho = inverted_dm
            else:
                sum_rho += inverted_dm

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
