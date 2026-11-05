# ==============================================================================
# CalSymPy (Team 4, Delta-T) — calculus.py
#
# Plain-English Summary:
# This module implements the multivariable calculus operations taught in MAT 112:
# 1. Partial Derivatives & Gradient Vector:
#    ∇T = <Tx, Ty> describes the rate and direction of fastest temperature rise.
#    The magnitude |∇T| = sqrt(Tx² + Ty²) gives the steepness of the temperature hill.
# 2. Second Derivative Test for Functions of Two Variables:
#    Calculates the Hessian discriminant D = Txx * Tyy - (Txy)².
#    - D > 0 and Txx < 0: The surface curves downward in all directions -> True Maximum.
#    - D > 0 and Txx > 0: The surface curves upward in all directions -> True Minimum.
#    - D < 0: The surface curves up in one direction and down in another -> Saddle Point.
#    - D == 0: The test is inconclusive (higher-order terms needed).
# 3. Vector Divergence & Fourier's Law:
#    Heat flux is F = -k * ∇T (heat flows hot -> cold).
#    Divergence div F = -k * (Txx + Tyy) = -k * ∇²T.
#    Positive divergence means heat is generated (heat source); negative means heat sink.
# ==============================================================================

import numpy as np


def compute_gradient_magnitude(Tx, Ty):
    """
    Calculate the Euclidean norm (magnitude) of the gradient vector:
    |∇T| = sqrt(Tx² + Ty²).
    
    Calculus interpretation:
    Represents the maximum directional derivative at the point.
    It indicates how steeply temperature changes per unit distance (in °C/cm).
    """
    return np.sqrt(np.asarray(Tx, dtype=float)**2 + np.asarray(Ty, dtype=float)**2)


def compute_discriminant(Txx, Tyy, Txy):
    """
    Compute the Hessian discriminant (Hessian determinant) for the second derivative test:
    D = Txx * Tyy - (Txy)².
    
    Calculus interpretation:
    Measures the product of principal curvatures minus the square of the mixed twist.
    """
    txx = np.asarray(Txx, dtype=float)
    tyy = np.asarray(Tyy, dtype=float)
    txy = np.asarray(Txy, dtype=float)
    return txx * tyy - (txy**2)


def classify_critical_point(Txx, Tyy, Txy, tolerance=1e-6):
    """
    Apply the second derivative test to classify a critical point where ∇T = 0.
    
    Calculus Steps:
    1. Compute discriminant D = Txx * Tyy - (Txy)².
    2. Check sign of D:
       - If D > 0 and Txx < 0:
         The surface is concave down in both directions. True local maximum.
       - If D > 0 and Txx > 0:
         The surface is concave up in both directions. True local minimum.
       - If D < 0:
         Opposite concavities along different axes. Saddle point (like a mountain pass).
       - If D == 0 (within tolerance):
         Test is inconclusive.
         
    Returns:
        tuple: (D_value, classification_str, explanation_str)
    """
    txx = float(Txx)
    tyy = float(Tyy)
    txy = float(Txy)
    D = txx * tyy - (txy**2)

    if D > tolerance:
        if txx < -tolerance:
            classification = "True Maximum"
            explanation = (
                f"Discriminant D = {D:.2f} > 0 and second derivative Txx = {txx:.2f} < 0. "
                "The temperature surface curves downwards in all directions, confirming a true local maximum."
            )
        elif txx > tolerance:
            classification = "True Minimum"
            explanation = (
                f"Discriminant D = {D:.2f} > 0 and second derivative Txx = {txx:.2f} > 0. "
                "The temperature surface curves upwards in all directions, confirming a true local minimum."
            )
        else:
            classification = "Inconclusive (Txx near zero)"
            explanation = f"Discriminant D = {D:.2f} > 0, but Txx = {txx:.4f} is near zero."
    elif D < -tolerance:
        classification = "Saddle Point"
        explanation = (
            f"Discriminant D = {D:.2f} < 0. The surface curves upwards along one path and "
            "downwards along another, characteristic of a saddle point."
        )
    else:
        classification = "Inconclusive"
        explanation = (
            f"Discriminant D = {D:.4f} ≈ 0. The second derivative test cannot classify this point; "
            "higher-order Taylor series terms would be required."
        )

    return D, classification, explanation


def compute_laplacian(Txx, Tyy):
    """
    Compute the Laplacian operator: ∇²T = Txx + Tyy.
    
    Calculus interpretation:
    Represents the sum of the unmixed second derivatives.
    A negative Laplacian indicates the point is warmer than its immediate surroundings.
    """
    return np.asarray(Txx, dtype=float) + np.asarray(Tyy, dtype=float)


def compute_flux_divergence(Txx, Tyy, k):
    """
    Compute the divergence of the heat flux vector field F = -k * ∇T in W/m³:
    div F = ∇ · (-k * ∇T) = -k * ∇²T.
    
    Units convention:
    - Coordinates x, y are in cm, so unmixed second derivatives Txx and Tyy are in °C/cm².
    - Converting to °C/m² requires scaling by (100 cm/m)² = 10,000.
    - Thermal conductivity k is in W/(m·K).
    - Resulting divergence div F is in W/m³.
    
    Physical & Calculus interpretation:
    - div F > 0: Heat is expanding outward from this point (acting as a heat source).
    - div F < 0: Heat is converging inward toward this point (acting as a heat sink).
    """
    laplacian_cm = compute_laplacian(Txx, Tyy)
    laplacian_m = laplacian_cm * 10000.0
    return -float(k) * laplacian_m


def is_critical_point(Tx, Ty, tolerance=1e-3):
    """
    Check if a point is a critical point by verifying that gradient ∇T ≈ <0, 0>.
    """
    grad_mag = np.sqrt(float(Tx)**2 + float(Ty)**2)
    return grad_mag <= tolerance
