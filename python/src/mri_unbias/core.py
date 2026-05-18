"""Core polynomial bias-field correction."""

from __future__ import annotations

from functools import lru_cache

import numpy as np


def mri_unbias(
    image: np.ndarray,
    mask: np.ndarray | None = None,
    degree: int = 3,
    *,
    eps: float | None = None,
    chunk_size: int = 1_000_000,
) -> tuple[np.ndarray, np.ndarray]:
    """Estimate and correct a smooth polynomial bias field.

    Parameters
    ----------
    image
        3D MRI image.
    mask
        Boolean mask defining a region assumed to have homogeneous intensity.
        If omitted, all voxels are used.
    degree
        Total degree of the 3D polynomial model.
    eps
        Optional minimum absolute bias-field magnitude used during division.
        If omitted, no clipping is applied.
    chunk_size
        Number of voxels to evaluate per chunk when building the full bias
        field. This limits peak memory use for large MRI volumes.

    Returns
    -------
    corrected, bias_field
        Bias-corrected image and estimated 3D bias field.
    """

    bias_field = fit_bias_field(image, mask, degree, chunk_size=chunk_size)
    denominator = bias_field
    if eps is not None:
        if eps <= 0:
            raise ValueError("eps must be positive when provided")
        denominator = np.where(np.abs(bias_field) < eps, np.nan, bias_field)
    with np.errstate(divide="ignore", invalid="ignore"):
        corrected = np.asarray(image, dtype=np.float64) / denominator
    return corrected, bias_field


def fit_bias_field(
    image: np.ndarray,
    mask: np.ndarray | None = None,
    degree: int = 3,
    *,
    chunk_size: int = 1_000_000,
) -> np.ndarray:
    """Fit a 3D polynomial to masked voxel intensities and evaluate it globally."""

    image = _as_3d_float(image)
    degree = _validate_degree(degree)
    mask = _validate_mask(mask, image.shape)

    finite = np.isfinite(image)
    fit_mask = mask & finite
    if not np.any(fit_mask):
        raise ValueError("mask does not contain any finite image voxels")

    x, y, z = _coordinate_grids(image.shape)
    design_masked = _design_matrix(x[fit_mask], y[fit_mask], z[fit_mask], degree)
    values = image[fit_mask]

    coefficients, *_ = np.linalg.lstsq(design_masked, values, rcond=None)

    flat_bias = _evaluate_polynomial_chunked(
        x.ravel(),
        y.ravel(),
        z.ravel(),
        degree,
        coefficients,
        chunk_size=chunk_size,
    )
    return flat_bias.reshape(image.shape)


@lru_cache(maxsize=None)
def polynomial_powers(degree: int) -> tuple[tuple[int, int, int], ...]:
    """Return all 3D polynomial exponents with total degree <= ``degree``."""

    degree = _validate_degree(degree)
    powers: list[tuple[int, int, int]] = []
    for total_degree in range(degree + 1):
        for px in range(total_degree + 1):
            for py in range(total_degree - px + 1):
                pz = total_degree - px - py
                powers.append((px, py, pz))
    return tuple(powers)


def _design_matrix(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    degree: int,
) -> np.ndarray:
    columns = [
        (x**px) * (y**py) * (z**pz)
        for px, py, pz in polynomial_powers(degree)
    ]
    return np.column_stack(columns)


def _evaluate_polynomial_chunked(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    degree: int,
    coefficients: np.ndarray,
    *,
    chunk_size: int,
) -> np.ndarray:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    out = np.empty(x.shape[0], dtype=np.float64)
    for start in range(0, x.shape[0], chunk_size):
        stop = min(start + chunk_size, x.shape[0])
        design = _design_matrix(x[start:stop], y[start:stop], z[start:stop], degree)
        out[start:stop] = design.dot(coefficients)
    return out


def _coordinate_grids(shape: tuple[int, int, int]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    axes = tuple(_normalized_axis(n) for n in shape)
    return np.meshgrid(*axes, indexing="ij")


def _normalized_axis(size: int) -> np.ndarray:
    if size == 1:
        return np.zeros(1, dtype=np.float64)
    return np.linspace(-1.0, 1.0, size, dtype=np.float64)


def _as_3d_float(image: np.ndarray) -> np.ndarray:
    image = np.asarray(image, dtype=np.float64)
    if image.ndim != 3:
        raise ValueError(f"image must be 3D, got shape {image.shape}")
    return image


def _validate_mask(mask: np.ndarray | None, shape: tuple[int, int, int]) -> np.ndarray:
    if mask is None:
        return np.ones(shape, dtype=bool)
    mask = np.asarray(mask, dtype=bool)
    if mask.shape != shape:
        raise ValueError(f"mask shape {mask.shape} does not match image shape {shape}")
    return mask


def _validate_degree(degree: int) -> int:
    if not isinstance(degree, (int, np.integer)):
        raise TypeError("degree must be an integer")
    degree = int(degree)
    if degree < 0:
        raise ValueError("degree must be non-negative")
    return degree
