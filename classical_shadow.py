import random
from abc import ABC, abstractmethod

import numpy as np
from qiskit import QuantumCircuit

from backrotation import (
    n_qubit_clifford_backrotation,
    single_qubit_clifford_backrotation,
)
from random_clifford import get_random_1qbit_clifford, get_random_nqbit_clifford

# TODO: maybe refactor beacause when nqbit clifford are added


class ClassicalShadow(ABC):
    def __init__(self, num_qubits: int, single_qubit_clifford: bool = True):
        self.num_qubits: int = num_qubits
        self.single_qubit_clifford: bool = single_qubit_clifford

        self.snapshots: list[list[np.ndarray]] = []

    def get_desity_matrix_from_snapshots(self):
        print("generating density matrix from snapshots")

    def get_orginal_destiny_matrix(self):
        print("getting original destiny matrix from state creation circuit")

    def add_snapshot(self):
        # get random rotation
        if self.single_qubit_clifford:
            rotations: list[str] = get_random_1qbit_clifford(self.num_qubits)
        else:
            rotations: list[str] = get_random_nqbit_clifford(self.num_qubits)

        state_circuit: QuantumCircuit = self.get_state_circuit()
        combined_circuit: QuantumCircuit = self.make_rotated_state_ciruit(
            rotations, state_circuit
        )

        # getting the measurement results for each qubit
        measurement_results = self.run_cuircuit_and_get_measurment(combined_circuit)

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

    def compute_snapshot(self, rotation_description, measurement):
        assert len(measurement) == self.num_qubits
        # measurement is a bitstring
        # rotation description is a list of single qubit clifford rotations
        if self.single_qubit_clifford:
            return single_qubit_clifford_backrotation(rotation_description, measurement)
        else:
            return n_qubit_clifford_backrotation(rotation_description, measurement)

    @abstractmethod
    def run_cuircuit_and_get_measurment(self, circuit):
        raise NotImplementedError("This function is not yet implemented.")

    @abstractmethod
    def get_state_circuit(self) -> QuantumCircuit:
        """ "Returns the quantum circuit that prepare the state of interest."""
        raise NotImplementedError("This method should be implemented by subclasses")
