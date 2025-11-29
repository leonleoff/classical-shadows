import random
from abc import ABC, abstractmethod

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix

from shadow_protocol import ShadowProtocol


class AbstractClassicalShadow(ABC):
    def __init__(self, shadow_protocol: ShadowProtocol):
        self.num_qubits: int = shadow_protocol.get_num_qubits()
        self.shadow_protocol: ShadowProtocol = shadow_protocol

        self.snapshots = []  # no type beacuse can be denstiy matrix or stabilzer

    def get_original_density_matrix(self):
        circuit = self.shadow_protocol.get_state_circuit()
        clean_circuit = circuit.copy()
        clean_circuit.remove_final_measurements()
        return DensityMatrix(clean_circuit).data

    def add_snapshot(self):
        rotations: list[str] = self.get_random_rotations(self.num_qubits)

        # prepare circuit
        state_circuit: QuantumCircuit = self.shadow_protocol.get_state_circuit()
        combined_circuit: QuantumCircuit = self.make_rotated_state_ciruit(
            rotations, state_circuit
        )

        # run circuit and getting the measurement results for each qubit
        measurement_results = self.shadow_protocol.run_cuircuit_and_get_measurment(
            combined_circuit
        )
        assert len(measurement_results) == self.num_qubits

        # roatet back and store snapshot
        snapshot = self.compute_snapshot(rotations, measurement_results)
        self.snapshots.append(snapshot)

    def predict_observable(self):
        raise NotImplementedError("This function is not yet implemented.")

    def make_rotated_state_ciruit(
        self, rotation_description, state_creation_circuit
    ) -> QuantumCircuit:
        circuit = state_creation_circuit.copy()
        for qubit_index in range(self.num_qubits):
            rotation = rotation_description[qubit_index]
            if rotation == "X":
                circuit.h(qubit_index)
            elif rotation == "Y":
                circuit.sdg(qubit_index)
                circuit.h(qubit_index)
            elif rotation == "Z":
                pass  # no rotation needed
            else:
                raise ValueError(f"Unknown rotation description: {rotation}")

        circuit.measure_all()
        return circuit

    @abstractmethod
    def compute_snapshot(self, rotation_description, measurement):
        raise NotImplementedError("This method should be implemented by subclasses")

    @abstractmethod
    def get_random_rotations(self, num_qubits) -> list[str]:
        raise NotImplementedError("This method should be implemented by subclasses")

    @abstractmethod
    def get_desity_matrix_from_snapshots(self):
        raise NotImplementedError("This method should be implemented by subclasses")
