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
        rotation_cuircuit = (
            self.create_tp_of_random_nqbit_clifford()
        )  # TODO using types here in a smart way
        state_genertaion_circuit = self.getStateCreationCircuit()
        combined_circuit = self.make_cirucit_that_ceates_rotated_state(
            rotation_cuircuit, state_genertaion_circuit
        )
        measurement = self.run_cuircuit_and_get_measurment(combined_circuit)
        snapshot = self.compute_snapshot(rotation_cuircuit, measurement)
        self.snapshots.append(snapshot)

    def predict_observable(self):
        raise NotImplementedError("This function is not yet implemented.")

    def make_cirucit_that_ceates_rotated_state(
        self, rotation_circuit, state_creation_circuit
    ):
        # TODO: check if qbit count is the same
        print("checking if qbit count is the same ")
        print("combining both circuits")

    def create_random_nqbit_clifford(self):
        # TODO: maybe there is something better than giving back a circuit as this is hard to back rotate
        """returns random n-qubit clifford circuits in the size of num_qubits"""
        raise NotImplementedError("This function is not yet implemented.")

    def create_tp_of_random_nqbit_clifford(self):
        # TODO: maybe there is something better than giving back a circuit as this is hard to back rotate
        """returns shadow_size x tesnorpoducts of random single qubit clifford measurements in the size of num_qubits"""
        print(
            f"making a tensor product of random single qubit clifford measurements size of {self.num_qubits}"
        )

    def compute_snapshot(self, rotation_circuit, measurement):
        print("generating snapshot")

    @abstractmethod
    def run_cuircuit_and_get_measurment(self, circuit):
        raise NotImplementedError("This function is not yet implemented.")

    @abstractmethod
    def getStateCreationCircuit(self):
        raise NotImplementedError("This method should be implemented by subclasses")
