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
    ) -> list[Clifford]:
        assert len(cliffords) == 1
        assert len(measurement_results) == self.num_qubits

        base_state_qc = QuantumCircuit(self.num_qubits)

        for i, bit in enumerate(measurement_results):
            if bit == 1:
                base_state_qc.x(i)

        base_cliff = Clifford(base_state_qc)

        pre_measurement_cliff = base_cliff.compose(cliffords[0].adjoint())

        qc_reverse = QuantumCircuit(self.num_qubits)
        for i in range(self.num_qubits // 2):
            qc_reverse.swap(i, self.num_qubits - 1 - i)

        clifford_reverse = Clifford(qc_reverse)
        reversed_cliff = pre_measurement_cliff.compose(clifford_reverse)

        return [reversed_cliff]

    def get_random_rotations(self, num_qubits):
        # S. Bravyi and D. Maslov, Hadamard-free circuits expose the structure of the Clifford group. https://arxiv.org/abs/2003.09412
        return [random_clifford(num_qubits)]

    def get_density_matrix_from_cliffords(self):
        if not self.clifford_list_list:
            raise ValueError("No snapshot present.")

        sum_rho = None
        for i, row in enumerate(self.clifford_list_list):
            assert len(row) == 1
            stab = StabilizerState(row[0])
            dm_data: DensityMatrix = self.stabilizer_to_density_matrix(stab)
            inverted_dm = ((2**self.num_qubits) + 1) * dm_data - np.eye(
                2**self.num_qubits
            )
            if sum_rho is None:
                sum_rho = inverted_dm
            else:
                sum_rho += inverted_dm

        return sum_rho / len(self.clifford_list_list)

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

    def calculate_fidelity(self, clifford_a: Clifford):
        n_qubits = self.num_qubits

        # change qbit order of input clifford
        qc_reverse = QuantumCircuit(n_qubits)
        for i in range(n_qubits // 2):
            qc_reverse.swap(i, n_qubits - 1 - i)
        clifford_reverse = Clifford(qc_reverse)

        clifford_a = clifford_a.compose(clifford_reverse)

        clifford_list_list = self.clifford_list_list
        overlaps: list[float] = []

        cliff_a_inv = clifford_a.adjoint()

        for cliff_list in clifford_list_list:
            assert len(cliff_list) == 1
            cliff_b: Clifford = cliff_list[0]

            # |<a|b>|^2
            combined_cliff = cliff_b.compose(cliff_a_inv)
            zero_state = StabilizerState(combined_cliff)

            probs = zero_state.probabilities_dict()
            overlap = probs.get("0" * n_qubits, 0.0)

            overlaps.append(overlap)

        if not overlaps:
            raise ValueError("Shadow list is empty.")

        mean_overlap = sum(overlaps) / len(overlaps)

        fidelity = (2**n_qubits + 1) * mean_overlap - 1

        return fidelity
