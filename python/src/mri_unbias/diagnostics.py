"""Diagnostics for polynomial degree selection."""

from __future__ import annotations

import numpy as np

from .core import mri_unbias


def degree_diagnostics(
    image: np.ndarray,
    mask: np.ndarray,
    degrees=range(1, 7),
    *,
    threshold_pct: float = 10.0,
    metric: str = "std",
) -> dict[str, np.ndarray | float | int | None]:
    """Evaluate white-matter uniformity across polynomial degrees.

    The returned ``best_degree`` is the previous degree before the first
    relative improvement below ``threshold_pct``. If no elbow is detected, it is
    the maximum tested degree.
    """

    degrees = np.asarray(list(degrees), dtype=int)
    if degrees.ndim != 1 or degrees.size == 0:
        raise ValueError("degrees must contain at least one polynomial degree")
    if np.any(degrees < 0):
        raise ValueError("degrees must be non-negative")

    values = np.empty(degrees.size, dtype=np.float64)
    for idx, degree in enumerate(degrees):
        corrected, _ = mri_unbias(image, mask, int(degree))
        masked_values = corrected[np.asarray(mask, dtype=bool)]
        if metric == "std":
            values[idx] = np.nanstd(masked_values)
        elif metric == "cov":
            values[idx] = np.nanstd(masked_values) / np.nanmean(masked_values)
        else:
            raise ValueError("metric must be 'std' or 'cov'")

    relative_improvement = -np.diff(values) / values[:-1] * 100.0
    below = np.flatnonzero(relative_improvement < threshold_pct)
    if below.size:
        elbow_idx = int(below[0] + 1)
        elbow_degree = int(degrees[elbow_idx])
        best_degree = int(degrees[elbow_idx - 1])
    else:
        elbow_degree = None
        best_degree = int(degrees[-1])

    return {
        "degrees": degrees,
        "metric_values": values,
        "relative_improvement_pct": relative_improvement,
        "threshold_pct": float(threshold_pct),
        "elbow_degree": elbow_degree,
        "best_degree": best_degree,
    }


def plot_degree_diagnostics(results: dict, ax=None):
    """Plot diagnostic results produced by :func:`degree_diagnostics`."""

    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError("plot_degree_diagnostics requires matplotlib") from exc

    if ax is None:
        _, ax = plt.subplots()

    degrees = np.asarray(results["degrees"])
    metric_values = np.asarray(results["metric_values"])
    improvements = np.asarray(results["relative_improvement_pct"])
    threshold = float(results["threshold_pct"])

    ax.plot(degrees, metric_values, "-o", label="WM metric")
    ax.set_xlabel("Polynomial degree")
    ax.set_ylabel("WM std or CoV")
    ax.grid(True)

    ax2 = ax.twinx()
    ax2.plot(degrees[1:], improvements, "--o", color="tab:orange", label="Improvement")
    ax2.axhline(threshold, color="tab:orange", linewidth=1)
    ax2.set_ylabel("Improvement (%)")

    elbow_degree = results.get("elbow_degree")
    best_degree = results.get("best_degree")
    if elbow_degree is not None:
        ax.axvline(elbow_degree, color="k", linestyle=":", label=f"Elbow = {elbow_degree}")
    if best_degree is not None:
        ax.axvline(best_degree, color="0.4", linestyle=":", label=f"Chosen = {best_degree}")

    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2)
    return ax
