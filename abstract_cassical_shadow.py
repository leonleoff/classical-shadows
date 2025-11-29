import random
from abc import ABC, abstractmethod

import numpy as np
from qiskit import QuantumCircuit


class AbstractClassicalShadow(ABC):
    def __init__(self, num_qubits: int):
        self.num_qubits: int = num_qubits

        self.snapshots = []  # no type beacuse can be denstiy matrix or stabilzer

    def get_desity_matrix_from_snapshots(self):
        print("generating density matrix from snapshots")

    def get_orginal_destiny_matrix(self):
        print("getting original destiny matrix from state creation circuit")

    def add_snapshot(self):
        rotations: list[str] = self.get_random_rotations(self.num_qubits)

        # prepare circuit
        state_circuit: QuantumCircuit = self.get_state_circuit()
        combined_circuit: QuantumCircuit = self.make_rotated_state_ciruit(
            rotations, state_circuit
        )

        # run circuit and getting the measurement results for each qubit
        measurement_results = self.run_cuircuit_and_get_measurment(combined_circuit)
        assert len(measurement_results) == self.num_qubits

        # roatet back and store snapshot
        snapshot = self.compute_snapshot(rotations, measurement_results)
        self.snapshots.append(snapshot)

    def predict_observable(self):
        raise NotImplementedError("This function is not yet implemented.")

    def make_rotated_state_ciruit(
        self, rotation_description, state_creation_circuit
    ) -> QuantumCircuit:
        print("checking if qbit count is the same ")
        print("makes a circuit out of description")
        print("combining both circuits")

    @abstractmethod
    def compute_snapshot(self, rotation_description, measurement):
        raise NotImplementedError("This method should be implemented by subclasses")

    @abstractmethod
    def run_cuircuit_and_get_measurment(self, circuit):
        raise NotImplementedError("This function is not yet implemented.")

    @abstractmethod
    def get_state_circuit(self) -> QuantumCircuit:
        """ "Returns the quantum circuit that prepare the state of interest."""
        raise NotImplementedError("This method should be implemented by subclasses")

    @abstractmethod
    def get_random_rotations(self, num_qubits) -> list[str]:
        raise NotImplementedError("This method should be implemented by subclasses")
