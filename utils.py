import numpy as np

def validate_dimensions(x, y):
    """
    Ensure both vectors have the same dimensions.
    Raises ValueError if lengths do not match.
    """
    if len(x) != len(y):
        raise ValueError(f"Vectors must have the same length. Got {len(x)} and {len(y)}")

def check_zero_vector(x):
    """
    Check if a vector is a zero vector.
    Raises ValueError if all elements are strictly zero.
    """
    if np.all(x == 0):
        raise ValueError("Operation cannot be performed on a zero vector.")
