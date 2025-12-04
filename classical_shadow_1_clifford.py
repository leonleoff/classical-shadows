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

from abstract_cassical_shadow import AbstractClassicalShadow


class ClassicalShadow_1_CLIFFORD(AbstractClassicalShadow):

    def compute_clifford_applied_to_measurements(
        self, cliffords: list[Clifford], measurement: list[int]
    ) -> list[StabilizerState]:
        assert len(cliffords) == len(measurement)

        stabilizer_states = []

        state_0 = StabilizerState(QuantumCircuit(1))
        qc_1 = QuantumCircuit(1)
        qc_1.x(0)
        state_1 = StabilizerState(qc_1)

        for cliff, bit in zip(cliffords, measurement):
            if bit == 1:
                base_state = state_1
            else:
                base_state = state_0

            state = base_state.copy()
            pre_measurement_state = state.evolve(cliff.adjoint())
            stabilizer_states.append(pre_measurement_state)

        return stabilizer_states

    def get_random_rotations(self, num_qubits) -> list[Clifford]:
        # Define the 3 efficient basis-change gates
        # 1. I (measures Z)
        # 2. H (measures X) -> H * X * H = Z
        # 3. H S^dag (measures Y) -> (H S^dag) * Y * (S H) = Z

        # Create the Cliffords
        # (Tip: For better performance, you could move this creation to __init__)
        c_z = Clifford(QuantumCircuit(1))  # Identity

        qc_x = QuantumCircuit(1)
        qc_x.h(0)
        c_x = Clifford(qc_x)

        qc_y = QuantumCircuit(1)
        qc_y.sdg(0)  # S-dagger
        qc_y.h(0)
        c_y = Clifford(qc_y)

        efficient_cliffords = [c_z, c_x, c_y]

        # Randomly select a basis for each qubit
        return [random.choice(efficient_cliffords) for _ in range(num_qubits)]

    def get_desity_matrix_from_stabilizers(self):
        if not self.stabilizer_list_list:
            raise ValueError("No stablizers prestent.")
        sum_rho = None

        for row in self.stabilizer_list_list:

            inverted_qubits = []

            for stab in row:
                dm_data = DensityMatrix(stab).data
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
