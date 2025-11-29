import random
from abc import ABC, abstractmethod

import numpy as np
from qiskit import QuantumCircuit

from backrotation import (
    n_qubit_clifford_backrotation,
    single_qubit_clifford_backrotation,
)
from random_clifford import get_random_nqbit_clifford, get_random_rotations


class ClassicalShadow_SINGLE_CLIFFORD(AbstractClassicalShadow):

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
