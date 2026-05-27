# mri-unbias Python package

Polynomial bias-field correction for 3D MRI data.

The Python implementation mirrors the MATLAB package: it fits a smooth 3D
polynomial to intensities inside a homogeneous mask, usually white matter,
evaluates the fitted bias field over the full volume, and divides the image by
that field.

## Install

From this directory:

```bash
pip install -e ".[all]"
```

For the core NumPy-only API:

```bash
pip install -e .
```

## Python API

```python
import nibabel as nib
from mri_unbias import mri_unbias

img_nii = nib.load("../example_data/t1_fl3d_FA30.nii.gz")
mask_nii = nib.load("../example_data/WM_mask.nii.gz")

img = img_nii.get_fdata()
wm_mask = mask_nii.get_fdata() > 0

corrected, bias_field = mri_unbias(img, wm_mask, degree=3)
```

Optional brain-mask stabilization:

```python
brain_mask = nib.load("brain_mask.nii.gz").get_fdata() > 0
corrected, bias_field = mri_unbias(
    img,
    wm_mask,
    degree=3,
    brain_mask=brain_mask,
)
```

Providing `brain_mask` does not change the polynomial fit. It restricts the
applied bias-field range outside the brain to the full min/max bias range
observed inside the brain mask. This is optional and mainly avoids absurd
polynomial extrapolation values outside the brain.

## Command line

```bash
mri-unbias \
  ../example_data/t1_fl3d_FA30.nii.gz \
  ../example_data/WM_mask.nii.gz \
  --degree 3 \
  --corrected ../example_data/output/python/t1_fl3d_FA30_unbiased_poly3.nii.gz \
  --bias-field ../example_data/output/python/t1_fl3d_FA30_bias_estimation_poly3.nii.gz
```

With optional outside-brain bias stabilization:

```bash
mri-unbias \
  image.nii.gz \
  wm_mask.nii.gz \
  --degree 3 \
  --brain-mask brain_mask.nii.gz \
  --corrected image_unbiased.nii.gz \
  --bias-field image_bias.nii.gz
```

To run the bundled example data from the source repository:

```bash
mri-unbias-example
```

This writes corrected NIfTI outputs and `before_after_visualization.png` under
`../example_data/output/python/`.
