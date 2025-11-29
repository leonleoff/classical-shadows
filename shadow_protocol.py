from abc import ABC, abstractmethod

from qiskit import QuantumCircuit


class ShadowProtocol(ABC):
    @abstractmethod
    def get_num_qubits(self) -> int:
        raise NotImplementedError("This method should be implemented by subclasses")

    @abstractmethod
    def get_state_circuit(self) -> QuantumCircuit:
        """ "Returns the quantum circuit that prepare the state of interest."""
        raise NotImplementedError("This method should be implemented by subclasses")

    @abstractmethod
    def run_cuircuit_and_get_measurment(self, circuit):
        raise NotImplementedError("This function is not yet implemented.")
