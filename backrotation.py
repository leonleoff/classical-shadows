def single_qubit_clifford_backrotation(rotation_description, measurement):
    print("computing backrotation for single qubit clifford")
    if rotation_description == "i":
        return measurement
    elif rotation_description == "h":
        return measurement
    elif rotation_description == "h,sdg":
        return measurement
    else:
        raise ValueError("Unknown rotation description")


def n_qubit_clifford_backrotation(rotation_description, measurement):
    raise NotImplementedError("This function is not yet implemented.")
