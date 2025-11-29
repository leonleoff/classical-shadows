import random
from abc import ABC, abstractmethod

import numpy as np
from qiskit import QuantumCircuit

from abstract_cassical_shadow import AbstractClassicalShadow


class ClassicalShadow_N_CLIFFORD(AbstractClassicalShadow):

    def compute_snapshot(self, rotations, measurement):
        # TODO: implement using the Stabilizer formalism for efficiency
        raise NotImplementedError("This method is not yet implemented.")

    def get_random_rotations(self, num_qubits) -> list[str]:
        raise NotImplementedError("This method is not yet implemented.")
