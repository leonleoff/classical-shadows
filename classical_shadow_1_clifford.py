import random
from functools import reduce

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import (
    Clifford,
    DensityMatrix,
    Pauli,
    SparsePauliOp,
    StabilizerState,
    Statevector,
    random_clifford,
)
from qiskit.visualization import array_to_latex

from abstract_cassical_shadow import AbstractClassicalShadow


class ClassicalShadow_1_CLIFFORD(AbstractClassicalShadow):

    def compute_clifford_applied_to_measurements(
        self, cliffords: list[Clifford], measurement_results: list[int]
    ) -> list[StabilizerState]:

        assert len(cliffords) == len(measurement_results)

        stabilizer_states: list[StabilizerState] = []

        qc_0 = QuantumCircuit(1)
        state_0 = StabilizerState(qc_0)

        qc_1 = QuantumCircuit(1)
        qc_1.x(0)
        state_1 = StabilizerState(qc_1)

        for i, (cliff, bit) in enumerate(zip(cliffords, measurement_results)):
            bit_val = int(bit)

            if bit_val == 1:
                base_state = state_1
            elif bit_val == 0:
                base_state = state_0
            else:
                error_msg = f"Invalid measurement result: {bit_val}. Expected 0 or 1."
                raise ValueError(error_msg)

            state = base_state.copy()

            pre_measurement_state: StabilizerState = state.evolve(cliff.adjoint())
            stabilizer_states.append(pre_measurement_state)

        return stabilizer_states

    def get_random_rotations(self, num_qubits) -> list[Clifford]:
        # S. Bravyi and D. Maslov, Hadamard-free circuits expose the structure of the Clifford group. https://arxiv.org/abs/2003.09412
        return [random_clifford(1) for _ in range(num_qubits)]

    def get_desity_matrix_from_stabilizers(self, log: bool = False):
        if not self.stabilizer_list_list:
            raise ValueError("No stablizers prestent.")
        sum_rho = None

        for i, row in enumerate(self.stabilizer_list_list):
            inverted_qubits = []

            for j, stab in enumerate(row):
                dm_data: DensityMatrix = self.stabilizer_to_density_matrix(stab)

                inverted_dm = 3 * dm_data - np.eye(2)

                inverted_qubits.append(inverted_dm)

            full_snapshot = reduce(np.kron, inverted_qubits)

            if sum_rho is None:
                sum_rho = full_snapshot
            else:
                sum_rho += full_snapshot

        return sum_rho / len(self.stabilizer_list_list)

    def make_rotated_state_circuit(
        self, cliffords: list[Clifford], state_creation_circuit: QuantumCircuit
    ) -> QuantumCircuit:
        assert len(cliffords) == state_creation_circuit.num_qubits

        combined_circuit = state_creation_circuit.copy()
        combined_circuit.remove_final_measurements()

        for qubit_index in range(self.num_qubits):
            clifford: Clifford = cliffords[qubit_index]
            clifford_circuit: QuantumCircuit = clifford.to_circuit()
            combined_circuit.compose(
                clifford_circuit, qubits=[qubit_index], inplace=True
            )

        combined_circuit.measure_all()
        return combined_circuit
