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

        result = op.conj().T @ state @ op
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
        measurement_results = self.shadow_protocol.run_cuircuit_and_get_measurment(
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

        if log:
            from IPython.display import display
            from qiskit.quantum_info import DensityMatrix, Operator, Statevector

            print("\n--- Logging for state ---")

            print("State setup (Original Circuit):")
            display(state_circuit.draw("mpl"))

            print("With random measurements (Rotated Circuit):")
            display(combined_circuit.draw("mpl"))

            print(f"Leaded to measurement output: {measurement_results}")

            print(f"\nDetailed Breakdown (Back-rotation):")
            print(f"This dirac notations describe the reconstructed state per qubit:")

            for i, (stab, cliff, bit) in enumerate(
                zip(stabilizers, cliffords, measurement_results)
            ):
                print(f"\n--- Qubit {i} ---")

                print("The applied Random Rotation (Clifford):")
                display(cliff.to_circuit().draw("mpl"))

                print(" As Matrix:")
                display(Operator(cliff).draw("latex"))

                print(f" Lead to measurement result: {bit}")

                # Debugging Checks
                print(f" Type of reconstructed stab object: {type(stab)}")

                print(f" And the back rotated state is:")

                try:
                    dm = self.stabilizer_to_density_matrix(stab)

                    # Trace Check (Der Beweis, ob es ein State oder Operator ist)
                    trace_val = dm.trace()
                    print(f"  Trace (must be 1.0): {trace_val:.2f}")

                    if abs(trace_val - 1.0) > 0.001:
                        print(
                            "  WARNUNG: Das ist KEIN gültiger Quantenzustand (Spur != 1)!"
                        )

                    display(array_to_latex(dm, prefix="Backrotated state = "))

                except Exception as e:
                    print(f"  ERROR visualizing state: {e}")

    def predict_observable(self):
        raise NotImplementedError("This function is not yet implemented.")

    def get_shadow_size(self) -> int:
        return len(self.stabilizer_list_list)

    @abstractmethod
    def make_rotated_state_circuit(
        self, cliffords, state_creation_circuit
    ) -> QuantumCircuit:
        raise NotImplementedError("This method should be implemented by subclasses")

    @abstractmethod
    def compute_clifford_applied_to_measurements(
        self, rotation_description, measurement
    ):
        raise NotImplementedError("This method should be implemented by subclasses")

    @abstractmethod
    def get_random_rotations(self, num_qubits):
        raise NotImplementedError("This method should be implemented by subclasses")

    @abstractmethod
    def get_desity_matrix_from_stabilizers(self):
        raise NotImplementedError("This method should be implemented by subclasses")
