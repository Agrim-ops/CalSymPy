# ==============================================================================
# CalSymPy (Team 4, Delta-T) — tests/test_feature8_heatflow.py
#
# Plain-English Summary:
# Unit tests for Feature 8: Heat Flux & Vector Field Divergence.
# Verifies:
# 1. Fourier's Law: Heat flux F = -k * ∇T flows away from hot regions toward cold regions
#    (negative gradient direction).
# 2. Vector Divergence: div F = -k * (Txx + Tyy) = -k * ∇²T.
#    - At a hotspot (concave down, ∇²T < 0), div F > 0, acting as a heat source.
#    - At a cold spot (concave up, ∇²T > 0), div F < 0, acting as a heat sink.
# 3. Both streamlines and divergence figures render cleanly with Matplotlib.
# ==============================================================================

import pytest
import matplotlib.pyplot as plt
from models import get_model
from calculus import compute_flux_divergence, compute_laplacian
from plots import plot_heat_flux_streamlines, plot_flux_divergence


def test_fourier_law_direction():
    """
    Verify Fourier's Law: Heat flows hot -> cold along -∇T.
    At (3, 2) in Model A, temperature decreases toward the right (Tx < 0).
    Heat flux Fx = -k * Tx must therefore be strictly positive (flowing rightward).
    """
    model_a = get_model('A')
    k = 0.29
    tx, ty = model_a.evaluate_gradient(3.0, 2.0)
    tx_val = float(tx)
    ty_val = float(ty)

    # Tx is negative (temp drops as x increases)
    assert tx_val < 0

    # Heat flux Fx = -k * Tx must be positive
    Fx = -k * tx_val
    assert Fx > 0


def test_divergence_heat_source_and_sink():
    """
    Verify divergence physics:
    - At hotspot peak (2, 2) of Model A: ∇²T = -120 < 0, so div F = -k * (-120) > 0 (Source).
    - At coldest corner (0, 4) of Model C2: ∇²T > 0, so div F < 0 (Sink).
    """
    k = 0.29

    # Hotspot source check (Model A at (2, 2))
    model_a = get_model('A')
    txx_a, tyy_a, _ = [float(v) for v in model_a.evaluate_hessian(2.0, 2.0)]
    div_a = compute_flux_divergence(txx_a, tyy_a, k)
    assert div_a > 0, "Hotspot peak must have positive divergence (heat source)"

    # Cold valley sink check (Model C2 at (0, 4) where T=10°C)
    model_c2 = get_model('C2')
    txx_c2, tyy_c2, _ = [float(v) for v in model_c2.evaluate_hessian(0.0, 4.0)]
    div_c2 = compute_flux_divergence(txx_c2, tyy_c2, k)
    assert div_c2 < 0, "Cold spot must have negative divergence (heat sink)"


def test_streamlines_and_divergence_plots():
    """Verify that both streamlines and divergence plots generate valid figures."""
    model_a = get_model('A')
    k = 0.29

    fig_stream = plot_heat_flux_streamlines(model_a, k=k)
    assert fig_stream is not None
    assert isinstance(fig_stream, plt.Figure)
    plt.close(fig_stream)

    fig_div = plot_flux_divergence(model_a, k=k)
    assert fig_div is not None
    assert isinstance(fig_div, plt.Figure)
    plt.close(fig_div)
