"""Optional NIfTI helpers."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .core import mri_unbias


def unbias_nifti(
    image_path: str | Path,
    mask_path: str | Path,
    corrected_path: str | Path,
    bias_field_path: str | Path,
    *,
    degree: int = 3,
) -> tuple[Path, Path]:
    """Run bias correction on NIfTI inputs and write corrected/bias outputs."""

    try:
        import nibabel as nib
    except ImportError as exc:
        raise ImportError("NIfTI I/O requires nibabel; install mri-unbias[io]") from exc

    image_nii = nib.load(str(image_path))
    mask_nii = nib.load(str(mask_path))

    image = image_nii.get_fdata(dtype=np.float64)
    mask = mask_nii.get_fdata() > 0
    corrected, bias_field = mri_unbias(image, mask, degree)

    corrected_path = Path(corrected_path)
    bias_field_path = Path(bias_field_path)
    corrected_path.parent.mkdir(parents=True, exist_ok=True)
    bias_field_path.parent.mkdir(parents=True, exist_ok=True)

    nib.save(
        _float32_nifti_like(corrected, image_nii, display_range=(0.0, 2.0)),
        str(corrected_path),
    )
    nib.save(
        _float32_nifti_like(bias_field, image_nii),
        str(bias_field_path),
    )
    return corrected_path, bias_field_path


def _float32_nifti_like(
    data: np.ndarray,
    reference_img,
    *,
    display_range: tuple[float, float] | None = None,
):
    try:
        import nibabel as nib
    except ImportError as exc:
        raise ImportError("NIfTI I/O requires nibabel; install mri-unbias[io]") from exc

    header = reference_img.header.copy()
    header.set_data_dtype(np.float32)
    header["scl_slope"] = 1
    header["scl_inter"] = 0
    if display_range is None:
        finite = np.asarray(data)[np.isfinite(data)]
        if finite.size:
            display_range = tuple(float(x) for x in np.percentile(finite, [1, 99]))
    if display_range is not None:
        header["cal_min"] = display_range[0]
        header["cal_max"] = display_range[1]
    return nib.Nifti1Image(
        np.asarray(data, dtype=np.float32),
        reference_img.affine,
        header,
    )
