import random
from abc import ABC, abstractmethod

import numpy as np
from qiskit import QuantumCircuit

from abstract_cassical_shadow import AbstractClassicalShadow


class ClassicalShadow_SINGLE_CLIFFORD(AbstractClassicalShadow):

    def compute_snapshot(self, rotations, measurement):
        # TODO: implement using the Stabilizer formalism for efficiency
        raise NotImplementedError("This method is not yet implemented.")

    def get_random_rotations(self, num_qubits) -> list[str]:
        raise NotImplementedError("This method is not yet implemented.")

    @abstractmethod
    def run_cuircuit_and_get_measurment(self, circuit):
        raise NotImplementedError("This function is not yet implemented.")

    @abstractmethod
    def get_state_circuit(self) -> QuantumCircuit:
        """ "Returns the quantum circuit that prepare the state of interest."""
        raise NotImplementedError("This method should be implemented by subclasses")
