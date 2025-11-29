def single_qubit_clifford_backrotation(rotation_description, measurement):
    assert len(rotation_description) == len(measurement)

    for i in range(len(rotation_description)):
        measurement[i] = backrotate_single_measurement(
            rotation_description[i], measurement[i]
        )


def backrotate_single_measurement(
    single_qubit_rotation_description, single_qubit_measurement
):
    if single_qubit_rotation_description == "h":
        if single_qubit_measurement == 0:
            return "x+"
        elif single_qubit_measurement == 1:
            return "x-"
        else:
            raise ValueError("Invalid measurement outcome")
    elif single_qubit_rotation_description == "h,sdg":
        if single_qubit_measurement == 0:
            return "y+"
        elif single_qubit_measurement == 1:
            return "y-"
        else:
            raise ValueError("Invalid measurement outcome")
    elif single_qubit_rotation_description == "id":
        if single_qubit_measurement == 0:
            return "z+"
        elif single_qubit_measurement == 1:
            return "z-"
        else:
            raise ValueError("Invalid measurement outcome")
    else:
        raise ValueError("Invalid rotation description")


def n_qubit_clifford_backrotation(rotation_description, measurement):
    raise NotImplementedError("This function is not yet implemented.")
