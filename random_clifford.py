import random


def get_random_nqbit_clifford(num_qubits):
    raise NotImplementedError("This function is not yet implemented.")


def get_random_singlequbit_clifford(num_qubits):
    return [random.choice(["i", "h", "h,sdg"]) for i in range(num_qubits)]
