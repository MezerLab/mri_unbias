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
        nib.Nifti1Image(corrected, image_nii.affine, image_nii.header),
        str(corrected_path),
    )
    nib.save(
        nib.Nifti1Image(bias_field, image_nii.affine, image_nii.header),
        str(bias_field_path),
    )
    return corrected_path, bias_field_path
