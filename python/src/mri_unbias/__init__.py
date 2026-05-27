"""Polynomial bias-field correction for 3D MRI images."""

from .core import (
    clip_bias_field_outside_mask,
    fit_bias_field,
    mri_unbias,
    polynomial_powers,
)
from .diagnostics import degree_diagnostics, plot_degree_diagnostics

__all__ = [
    "clip_bias_field_outside_mask",
    "degree_diagnostics",
    "fit_bias_field",
    "mri_unbias",
    "plot_degree_diagnostics",
    "polynomial_powers",
]

__version__ = "0.1.0"
