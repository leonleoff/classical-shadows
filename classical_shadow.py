import random
from abc import ABC, abstractmethod


class ClassicalShadow(ABC):
    def __init__(self, data):
        self.snapshots = []

    def get_desity_matrix_from_snapshots(self):
        print("generating density matrix from snapshots")

    def get_orginal_destiny_matrix(self):
        print("getting original destiny matrix from state creation circuit")

    def add_snapshot(self, num_qubits):
        self.num_qubits = num_qubits
        rotation_description = self.create_description_tp_of_random_nqbit_clifford()
        state_genertaion_circuit = self.getStateCreationCircuit()
        combined_circuit = self.make_cirucit_that_ceates_rotated_state(
            rotation_description, state_genertaion_circuit
        )
        measurement = self.run_cuircuit_and_get_measurment(combined_circuit)
        snapshot = self.compute_snapshot(rotation_description, measurement)
        self.snapshots.append(snapshot)

    def predict_observable(self):
        raise NotImplementedError("This function is not yet implemented.")

    def make_cirucit_that_ceates_rotated_state(
        self, rotation_description, state_creation_circuit
    ):
        print("checking if qbit count is the same ")
        print("makes a circuit out of description")
        print("combining both circuits")

    def create_random_nqbit_clifford(self):
        # TODO: maybe there is something better than giving back a circuit as this is hard to back rotate
        """returns random n-qubit clifford circuits in the size of num_qubits"""
        raise NotImplementedError("This function is not yet implemented.")

    def create_description_tp_of_random_nqbit_clifford(self):
        # TODO: maybe later enum
        # TODO: check if I H SH is correct
        return [random.choice(["I", "H", "SH"]) for i in range(self.num_qubits)]

    def compute_snapshot(self, rotation_description, measurement):
        # measurement is a bitstring
        # rotation description is a list of single qubit clifford rotations
        print("")

    @abstractmethod
    def run_cuircuit_and_get_measurment(self, circuit):
        raise NotImplementedError("This function is not yet implemented.")

    @abstractmethod
    def getStateCreationCircuit(self):
        raise NotImplementedError("This method should be implemented by subclasses")
