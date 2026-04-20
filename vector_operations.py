import numpy as np
from utils import validate_dimensions, check_zero_vector

def inner_product_manual(x, y):
    """
    Computes the dot product manually.
    Mathematically: <x, y> = sum(x_i * y_i)
    """
    validate_dimensions(x, y)
    return sum(float(xi) * float(yi) for xi, yi in zip(x, y))

def inner_product_numpy(x, y):
    """
    Computes the dot product using NumPy.
    """
    validate_dimensions(x, y)
    return np.dot(x, y)

def compute_norm(x):
    """
    Computes the L2 norm (energy) of the signal.
    Mathematically: ||x|| = sqrt(<x, x>)
    """
    return np.sqrt(inner_product_numpy(x, x))

def normalize(x):
    """
    Normalizes a vector to have unit norm.
    """
    norm_x = compute_norm(x)
    if norm_x == 0:
        check_zero_vector(x)
    return x / norm_x

def is_orthogonal(x, y, tolerance=1e-6):
    """
    Checks if two vectors are orthogonal based on their inner product.
    Returns True if abs(<x, y>) < tolerance.
    """
    validate_dimensions(x, y)
    dot_prod = inner_product_numpy(x, y)
    return abs(dot_prod) < tolerance

def project(x, y):
    """
    Projects vector x onto vector y.
    Formula: Proj_y(x) = (<x, y> / <y, y>) * y
    """
    validate_dimensions(x, y)
    check_zero_vector(y)
    
    dot_xy = inner_product_numpy(x, y)
    dot_yy = inner_product_numpy(y, y)
    
    if dot_yy == 0:
        raise ValueError("Cannot project onto a zero-energy signal.")
        
    return (dot_xy / dot_yy) * y

def gram_schmidt(vectors):
    """
    Bonus: Gram-Schmidt orthogonalization for a list of vectors.
    Converts a set of linearly independent vectors into an orthonormal basis.
    """
    if not vectors:
        return []
    
    orthogonal_basis = []
    for v in vectors:
        w = np.copy(v)
        for b in orthogonal_basis:
            w = w - project(v, b)
            
        # Only add if w is not a zero vector (linearly independent)
        if compute_norm(w) > 1e-10:
            orthogonal_basis.append(normalize(w))
            
    return orthogonal_basis
