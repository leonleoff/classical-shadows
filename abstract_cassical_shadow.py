import random
from abc import ABC, abstractmethod

import numpy as np
import qiskit.qasm2
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Clifford, DensityMatrix, StabilizerState, Statevector
from qiskit.visualization import array_to_latex
from qiskit_aer import AerSimulator

from shadow_protocol import ShadowProtocol


class AbstractClassicalShadow(ABC):
    def __init__(self, shadow_protocol: ShadowProtocol):
        self.num_qubits: int = shadow_protocol.get_num_qubits()
        self.shadow_protocol: ShadowProtocol = shadow_protocol

        self.stabilizer_list_list: list[list[StabilizerState]] = []

    @staticmethod
    def stabilizer_to_density_matrix(stab: StabilizerState) -> DensityMatrix:
        op = stab.to_operator().data

        state = np.zeros_like(op)  # same shape, all zeros
        state[0, 0] = 1

        result = op @ state @ op.conj().T
        return result

    def get_original_density_matrix(self):
        circuit: QuantumCircuit = self.shadow_protocol.get_state_circuit()
        clean_circuit = circuit.copy()
        clean_circuit.remove_final_measurements()
        rho = DensityMatrix(clean_circuit)
        return rho.reverse_qargs().data

    def add_snapshot(self, log: bool = False):
        cliffords: list[Clifford] = self.get_random_rotations(self.num_qubits)

        # prepare circuit
        state_circuit: QuantumCircuit = self.shadow_protocol.get_state_circuit()
        combined_circuit: QuantumCircuit = self.make_rotated_state_circuit(
            cliffords, state_circuit
        )

        # run circuit and getting the measurement results for each qubit
        measurement_results = self.shadow_protocol.run_circuit_and_get_measurement(
            combined_circuit
        )

        assert len(measurement_results) == self.num_qubits

        # roatet back and store snapshot
        stabilizers: list[StabilizerState] = (
            self.compute_clifford_applied_to_measurements(
                cliffords, measurement_results
            )
        )
        self.stabilizer_list_list.append(stabilizers)

    def get_shadow_size(self) -> int:
        return len(self.stabilizer_list_list)

    def predict_observable(self):
        raise NotImplementedError("This function is not yet implemented.")

    @abstractmethod
    def make_rotated_state_circuit(
        self, cliffords, state_creation_circuit
    ) -> QuantumCircuit:
        raise NotImplementedError("This method should be implemented by subclasses")

    @abstractmethod
    def compute_clifford_applied_to_measurements(self, cliffords, measurement_results):
        raise NotImplementedError("This method should be implemented by subclasses")

    @abstractmethod
    def get_random_rotations(self, num_qubits):
        raise NotImplementedError("This method should be implemented by subclasses")

    @abstractmethod
    def get_density_matrix_from_stabilizers(self):
        raise NotImplementedError("This method should be implemented by subclasses")

    @abstractmethod
    def calculate_fidelity(self):
        raise NotImplementedError("This method should be implemented by subclasses")
