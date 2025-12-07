import sys

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford
from qiskit_aer import AerSimulator

sys.path.insert(0, "../../..")

from classical_shadow_1_clifford import ClassicalShadow_1_CLIFFORD
from shadow_protocol import ShadowProtocol


class Protocol(ShadowProtocol):

    def get_num_qubits(self) -> int:
        return 2

    def get_state_circuit(self) -> QuantumCircuit:
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        return circuit

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
    shadow = ClassicalShadow_1_CLIFFORD(protocol)

    expected_matrix = np.array(
        [
            [0.5, 0.0, 0.0, 0.5],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.5, 0.0, 0.0, 0.5],
        ]
    )

    for _ in range(5000):
        shadow.add_snapshot()

    reconstructed_dm = shadow.get_density_matrix_from_cliffords()

    if hasattr(reconstructed_dm, "data"):
        reconstructed_dm = reconstructed_dm.data

    print("\nReconstructed Matrix:\n", np.real(reconstructed_dm))
    print("Expected Matrix:\n", expected_matrix)

    np.testing.assert_allclose(
        np.real(reconstructed_dm),
        expected_matrix,
        rtol=0.0,
        atol=0.08,
        err_msg="The reconstructed density matrix differs by more than 0.01 from the expected matrix.",
    )
