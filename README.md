# `MRI_UNBIAS`: Polynomial Bias Field Correction for MRI Data

**Author:** Elior Drori
**Lab:** Mezer Lab, The Hebrew University of Jerusalem
**Year:** 2023

---

## Overview

`mri_unbias` is a MATLAB function for estimating and correcting intensity bias fields in 3D brain MRI images.
It fits an *n-th degree 3D polynomial* to voxel intensities within a region assumed to be uniform (typically a white-matter mask).
This polynomial models the smooth spatial bias field that corrupts MRI signal intensity.
The estimated bias is then used to correct the full image.

---

## Function Summary

```matlab
[img_corrected, bias_field] = mri_unbias(image, wm_mask, n_degree)
```

### Inputs

| Name          | Description                                                         |
| ------------- | ------------------------------------------------------------------- |
| `img`         | 3D MRI image (e.g., T1-weighted volume)                             |
| `wm_mask`     | Binary 3D mask defining the homogeneous region (i.e., white matter) |
| `poly_degree` | Degree of the 3D polynomial bias model (default: 3)                 |

### Outputs

| Name              | Description                                              |
| ----------------- | -------------------------------------------------------- |
| `img_corrected`   | Bias-corrected 3D image                                  |
| `bias_field`      | Estimated 3D bias field (same dimensions as input image) |

---

## Method

1. The algorithm assumes that intensity variations within the mask arise solely from bias field inhomogeneity.
2. It fits a smooth 3D polynomial of degree `poly_degree` to the intensities within the mask using the PolyfitnTools package.
3. The fitted polynomial is evaluated over the entire image to estimate the bias field.
4. The original image is divided by this bias field to produce a corrected image.

---

## Dependencies

This function requires the **PolyfitnTools** package available on the MATLAB File Exchange:

[PolyfitnTools](https://www.mathworks.com/matlabcentral/fileexchange/34765-polyfitn)

Make sure both `polyfitn.m` and `polyvaln.m` are in your MATLAB path.

---

## Example Usage

A complete example script is provided:
`run_mri_unbias_example.m`

### Run it:

```matlab
run_mri_unbias_example
```

This example:

* Loads a sample T1-weighted image and a white-matter mask.
* Runs bias correction with a 3rd-degree polynomial.
* Saves the corrected image and bias field as NIfTI files.
* Generates a before-after visualization figure.
* Performs diagnostic analysis to evaluate the optimal polynomial degree.

Outputs are saved in:

```
example_data/output/
```

---

## Example Output Files

| File                                          | Description                                     |
| --------------------------------------------- | ----------------------------------------------- |
| `t1_fl3d_FA30_unbiased_poly3.nii.gz`          | Corrected image                                 |
| `t1_fl3d_FA30_bias_estimation_poly3.nii.gz`   | Estimated bias field                            |
| `before_after_visualization.png`              | Visualization comparing raw vs. corrected image |
| `diagnostics_polynomial_degree_selection.png` | Diagnostic elbow plot for degree selection      |
---

## Polynomial Degree Diagnostics

The example script includes an optional **Polynomial Degree Diagnostics** section, which provides a complementary analysis for selecting a suitable polynomial degree.
This diagnostic helps verify that the chosen degree adequately models the bias without overfitting.

The diagnostics routine:

1. Tests multiple polynomial degrees (e.g., 1–6).
2. Runs bias correction for each degree using `mri_unbias`.
3. Measures white-matter intensity uniformity (standard deviation).
4. Computes relative improvement between successive degrees.
5. Plots an **“elbow analysis”** showing when improvements become negligible (default threshold: 10%).
6. Marks both the elbow degree (where improvements fall below threshold) and the chosen degree (the last meaningful improvement before that).

A diagnostic figure is automatically saved as:
   `diagnostics_polynomial_degree_selection.png`.


### Recommended Range and Interpretation

In typical brain MRI, the bias field is smooth and slowly varying across the brain.
Therefore, **low-degree polynomials (typically 1–3)** capture this field well.
Higher degrees rarely provide substantial additional benefit and may begin to overfit anatomical variability rather than true bias.


Thus:

> The diagnostic plot is *complementary* to domain knowledge —
> it can confirm that the practical, plausible range of **1–3 degrees** is already sufficient for most brain scans.

If the diagnostic plot shows only marginal improvement beyond this range, degree 2 or 3 should be selected.

---

## Notes

* The choice of polynomial degree balances **model smoothness** and **flexibility**.
  Use the diagnostic plot to confirm that improvements stabilize beyond degree 2–3.
* The method assumes the white-matter region is approximately homogeneous in intensity.
  While biological variability exists, this assumption provides a useful simplification for estimating the smooth bias field.
* **Limitation:** Because the bias field is estimated based on the white-matter region,
  this approach **should not be used if the study directly analyzes white-matter intensities**.
  In such cases, bias estimation from CSF, or a different bias-correction approach should be used instead.

---

## Citation

If you use this function in your research, please cite:

> Drori, E., Mezer Lab, The Hebrew University of Jerusalem (2023).
> *MRI_UNBIAS: Polynomial bias field correction for MRI data.*


