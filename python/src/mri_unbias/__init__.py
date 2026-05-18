"""Polynomial bias-field correction for 3D MRI images."""

from .core import fit_bias_field, mri_unbias, polynomial_powers
from .diagnostics import degree_diagnostics, plot_degree_diagnostics

__all__ = [
    "degree_diagnostics",
    "fit_bias_field",
    "mri_unbias",
    "plot_degree_diagnostics",
    "polynomial_powers",
]

__version__ = "0.1.0"
