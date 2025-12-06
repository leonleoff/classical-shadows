import sys

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford
from qiskit_aer import AerSimulator

sys.path.insert(0, "../../..")

from classical_shadow_1_clifford import ClassicalShadow_1_CLIFFORD
from shadow_protocol import ShadowProtocol


class ClassicalShadow(ClassicalShadow_1_CLIFFORD):

    def get_random_rotations(self, num_qubits) -> list[Clifford]:
        c_i = Clifford(QuantumCircuit(1))  # Identity
        return [c_i for _ in range(num_qubits)]


class Protocol(ShadowProtocol):

    def get_num_qubits(self) -> int:
        return 2

    def get_state_circuit(self) -> QuantumCircuit:
        return QuantumCircuit(2)

    def run_circuit_and_get_measurement(self, circuit) -> list[int]:
        sim = AerSimulator()

        job = sim.run(circuit, shots=997)
        result = job.result()
        counts = result.get_counts()
        max_hits = max(counts, key=counts.get)
        bit_list = [int(bit) for bit in list(max_hits)]

        return bit_list[::-1]


def test_reconstruction_with_identity():
    protocol = Protocol()
    shadow = ClassicalShadow(protocol)

    expected_matrix = np.array(
        [[4, 0, 0, 0], [0, -2, 0, 0], [0, 0, -2, 0], [0, 0, 0, 1]]
    )

    for _ in range(5):
        shadow.add_snapshot()

    reconstructed_dm = shadow.get_density_matrix_from_stabilizers()

    if hasattr(reconstructed_dm, "data"):
        reconstructed_dm = reconstructed_dm.data

    print("\nReconstructed Matrix:\n", np.real(reconstructed_dm))
    print("Expected Matrix:\n", expected_matrix)

    np.testing.assert_allclose(
        np.real(reconstructed_dm),
        expected_matrix,
        atol=1e-5,
        err_msg="The reconstructed density matrix does not match the expected theoretical matrix.",
    )
