import random
from functools import reduce

import numpy as np
from qiskit import QuantumCircuit

from abstract_cassical_shadow import AbstractClassicalShadow


class ClassicalShadow_1_CLIFFORD(AbstractClassicalShadow):

    def compute_snapshot(self, rotations, measurement):
        assert len(rotations) == len(measurement)
        list_of_density_matrices: list[np.ndarray] = []

        for i in range(len(rotations)):
            density_matrix = get_state_for_measurment(rotations[i], measurement[i])
            density_matrix = inverse_M_1(density_matrix)
            list_of_density_matrices.append(density_matrix)

        return list_of_density_matrices

    def get_random_rotations(self, num_qubits) -> list[str]:
        return [random.choice(["Z", "Y", "X"]) for i in range(num_qubits)]

    def get_desity_matrix_from_snapshots(self):
        if not self.snapshots:
            raise ValueError("No snapshot prestent.")

        first_snapshot_full = reduce(np.kron, self.snapshots[0])
        sum_rho = np.zeros_like(first_snapshot_full, dtype=complex)

        for snapshot_list in self.snapshots:
            full_snapshot = reduce(np.kron, snapshot_list)
            sum_rho += full_snapshot

        return sum_rho / len(self.snapshots)


# Backrotation


# Z-Basis (id): |0><0| und |1><1|
RHO_Z_PLUS = np.array([[1, 0], [0, 0]], dtype=complex)
RHO_Z_MINUS = np.array([[0, 0], [0, 1]], dtype=complex)

# X-Basis (h): |+><+| und |-><-|
# |+> = 1/sqrt(2) * (|0> + |1>)
RHO_X_PLUS = np.array([[0.5, 0.5], [0.5, 0.5]], dtype=complex)
RHO_X_MINUS = np.array([[0.5, -0.5], [-0.5, 0.5]], dtype=complex)

# Y-Basis (h,sdg): |+i><+i| und |-i><-i|
# |+i> = 1/sqrt(2) * (|0> + i|1>)
RHO_Y_PLUS = np.array([[0.5, -0.5j], [0.5j, 0.5]], dtype=complex)
RHO_Y_MINUS = np.array([[0.5, 0.5j], [-0.5j, 0.5]], dtype=complex)


def get_state_for_measurment(
    single_qubit_rotation_description, single_qubit_measurement
) -> np.ndarray:

    if single_qubit_rotation_description == "X":
        if single_qubit_measurement == 0:
            return RHO_X_PLUS
        elif single_qubit_measurement == 1:
            return RHO_X_MINUS
        else:
            raise ValueError("Invalid measurement outcome (must be 0 or 1)")

    elif single_qubit_rotation_description == "Y":
        if single_qubit_measurement == 0:
            return RHO_Y_PLUS
        elif single_qubit_measurement == 1:
            return RHO_Y_MINUS
        else:
            raise ValueError("Invalid measurement outcome (must be 0 or 1)")

    elif single_qubit_rotation_description == "Z":
        if single_qubit_measurement == 0:
            return RHO_Z_PLUS
        elif single_qubit_measurement == 1:
            return RHO_Z_MINUS
        else:
            raise ValueError("Invalid measurement outcome (must be 0 or 1)")

    else:
        raise ValueError(
            f"Invalid rotation description: {single_qubit_rotation_description}"
        )


def inverse_M_1(density_matrix: np.ndarray) -> np.ndarray:

    # Calculate the snapshot using the formula for n=1
    # 3 * rho - Identity
    snapshot = 3 * density_matrix - np.eye(2, dtype=complex)

    return snapshot
