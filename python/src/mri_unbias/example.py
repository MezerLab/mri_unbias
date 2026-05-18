"""Bundled example workflow."""

from __future__ import annotations

import os
from pathlib import Path

from .io import unbias_nifti


def main() -> int:
    repo_dir = _find_repo_dir()
    example_dir = repo_dir / "example_data"
    output_dir = example_dir / "output" / "python"
    degree = 3

    corrected_path = output_dir / f"t1_fl3d_FA30_unbiased_poly{degree}.nii.gz"
    bias_field_path = output_dir / f"t1_fl3d_FA30_bias_estimation_poly{degree}.nii.gz"

    unbias_nifti(
        example_dir / "t1_fl3d_FA30.nii.gz",
        example_dir / "WM_mask.nii.gz",
        corrected_path,
        bias_field_path,
        degree=degree,
    )

    visualization_path = output_dir / "before_after_visualization.png"
    _write_before_after_visualization(
        example_dir / "t1_fl3d_FA30.nii.gz",
        corrected_path,
        visualization_path,
    )

    print(f"Wrote corrected image: {corrected_path}")
    print(f"Wrote bias field: {bias_field_path}")
    print(f"Wrote visualization: {visualization_path}")
    return 0


def _write_before_after_visualization(
    image_path: Path,
    corrected_path: Path,
    visualization_path: Path,
) -> None:
    try:
        import nibabel as nib
    except ImportError as exc:
        raise ImportError(
            "The bundled example requires nibabel; install mri-unbias[io]."
        ) from exc

    os.environ.setdefault("MPLCONFIGDIR", str(visualization_path.parent / ".matplotlib"))
    try:
        import matplotlib
    except ImportError as exc:
        raise ImportError(
            "The bundled visualization requires matplotlib; install mri-unbias[plots]."
        ) from exc

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    image = nib.load(str(image_path)).get_fdata()
    corrected = nib.load(str(corrected_path)).get_fdata()
    slice_idx = 78 if image.shape[2] > 78 else image.shape[2] // 2

    fig, axes = plt.subplots(1, 2, figsize=(10, 5), facecolor="white")
    axes[0].imshow(_rotate_for_display(image[:, :, slice_idx]), cmap="gray", vmin=0, vmax=300)
    axes[0].set_title("Raw T1w Image")
    axes[1].imshow(_rotate_for_display(corrected[:, :, slice_idx]), cmap="gray", vmin=0, vmax=2)
    axes[1].set_title("Unbiased T1w Image")

    for ax in axes:
        ax.axis("off")
        ax.text(
            5,
            5,
            f"Slice {slice_idx}",
            color="white",
            va="top",
            fontweight="bold",
        )

    fig.tight_layout()
    visualization_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(visualization_path, dpi=150)
    plt.close(fig)


def _rotate_for_display(image_slice):
    import numpy as np

    return np.rot90(image_slice)


def _find_repo_dir() -> Path:
    candidates = [Path.cwd(), Path(__file__).resolve()]
    for start in candidates:
        for path in [start, *start.parents]:
            if (
                (path / "example_data" / "t1_fl3d_FA30.nii.gz").exists()
                and (path / "example_data" / "WM_mask.nii.gz").exists()
            ):
                return path
    raise FileNotFoundError(
        "Could not find example_data/. Run this command from the source repository "
        "or use mri-unbias with explicit input paths."
    )
