import random


def get_random_nqbit_clifford(num_qubits) -> list[str]:
    raise NotImplementedError("This function is not yet implemented.")


def get_random_rotations(num_qubits) -> list[str]:
    return [random.choice(["Z", "H", "X"]) for i in range(num_qubits)]
