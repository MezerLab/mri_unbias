# `MRI_UNBIAS`: Polynomial Bias Field Correction for MRI Data

**Author:** Elior Drori  
**Lab:** Mezer Lab, The Hebrew University of Jerusalem  
**Year:** 2023

---

## Overview

`mri_unbias` estimates and corrects smooth intensity bias fields in 3D brain MRI
images. It fits an n-th degree 3D polynomial to voxel intensities inside a
region assumed to be homogeneous, typically a white-matter mask. The fitted
polynomial models the spatial bias field, which is then evaluated over the full
image and used to correct the original volume.

This repository contains two implementations of the same method:

```text
matlab/   MATLAB implementation and example script
python/   Python package, CLI, examples, and tests
example_data/   Shared example NIfTI image and white-matter mask
```

---

## Method

1. Provide a 3D MRI image and a binary mask for a homogeneous tissue region.
2. Fit a smooth 3D polynomial of degree `poly_degree` to the masked intensities.
3. Evaluate the polynomial across the full image to estimate the bias field.
4. Divide the image by the estimated bias field.

The key assumption is that intensity variation inside the mask primarily
reflects scanner/acquisition bias rather than biological variation.

---

## Quick Start

Run the MATLAB example:

```matlab
addpath('matlab')
mri_unbias_example
```

Run the Python example:

```bash
mri-unbias-example
```

This writes corrected NIfTI outputs and a before/after visualization under
`example_data/output/python/`.

Run the Python CLI on explicit NIfTI inputs:

```bash
mri-unbias \
  example_data/t1_fl3d_FA30.nii.gz \
  example_data/WM_mask.nii.gz \
  --degree 3 \
  --corrected example_data/output/python/t1_fl3d_FA30_unbiased_poly3.nii.gz \
  --bias-field example_data/output/python/t1_fl3d_FA30_bias_estimation_poly3.nii.gz
```

---

## MATLAB Usage

Main function:

```matlab
[img_corrected, bias_field] = mri_unbias(img, wm_mask, poly_degree)
```

The MATLAB implementation requires **PolyfitnTools** from MATLAB File Exchange:

https://www.mathworks.com/matlabcentral/fileexchange/34765-polyfitn

Make sure both `polyfitn.m` and `polyvaln.m` are in your MATLAB path.

Example:

```matlab
addpath('matlab')
mri_unbias_example
```

The example loads the shared data in `example_data/`, writes corrected NIfTI
outputs, generates a before/after visualization, and runs polynomial-degree
diagnostics.

---

## Python Usage

Install the Python package from the `python/` directory:

```bash
cd python
pip install -e ".[all]"
```

Core NumPy API:

```python
import nibabel as nib
from mri_unbias import mri_unbias

img_nii = nib.load("../example_data/t1_fl3d_FA30.nii.gz")
mask_nii = nib.load("../example_data/WM_mask.nii.gz")

img = img_nii.get_fdata()
wm_mask = mask_nii.get_fdata() > 0

img_corrected, bias_field = mri_unbias(img, wm_mask, degree=3)
```

Command-line NIfTI workflow:

```bash
mri-unbias \
  ../example_data/t1_fl3d_FA30.nii.gz \
  ../example_data/WM_mask.nii.gz \
  --degree 3 \
  --corrected ../example_data/output/python/t1_fl3d_FA30_unbiased_poly3.nii.gz \
  --bias-field ../example_data/output/python/t1_fl3d_FA30_bias_estimation_poly3.nii.gz
```

Run the bundled example data from the source repository:

```bash
mri-unbias-example
```

Python tests:

```bash
cd python
pytest
```

---

## Example Output Files

Outputs are saved in separate implementation-specific folders:

```text
example_data/output/matlab/
example_data/output/python/
```

| File                                          | Description                                     |
| --------------------------------------------- | ----------------------------------------------- |
| `t1_fl3d_FA30_unbiased_poly3.nii.gz`          | Corrected image                                 |
| `t1_fl3d_FA30_bias_estimation_poly3.nii.gz`   | Estimated bias field                            |
| `before_after_visualization.png`              | Before/after visualization                      |
| `diagnostics_polynomial_degree_selection.png` | MATLAB diagnostic elbow plot                    |

---

## Polynomial Degree Diagnostics

The diagnostics test multiple polynomial degrees, run bias correction for each
degree, and measure intensity uniformity inside the mask using white-matter
standard deviation or coefficient of variation. The elbow point is the first
degree where the relative improvement falls below a threshold, with 10% used by
default.

In typical brain MRI, the bias field is smooth and slowly varying across the
brain. Low-degree polynomials, typically degree 1-3, are usually sufficient.
Higher degrees may begin to fit anatomical variability rather than true bias.

---

## Notes

* The choice of polynomial degree balances smoothness and flexibility.
* The method assumes the mask region is approximately homogeneous in intensity.
* Because the bias field is estimated from white matter, this approach should
  not be used when the study directly analyzes white-matter intensities. In that
  case, estimate the bias from another reference tissue or use a different
  correction approach.

---

## Citation

This toolbox is first introduced in Drori et. al., 2026 (preprint). If you use
this toolbox in your research, please cite:

> Drori, E., Kurer, N., and Mezer, AA.  
> Sensorimotor basal ganglia circuit asymmetry explains lateralized motor
> dysfunction in early Parkinson's disease.  
> bioRxiv (2026)
