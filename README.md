# `MRI_UNBIAS`: Polynomial Bias Field Correction for MRI Data

**Author:** Elior Drori
**Lab:** Mezer Lab, The Hebrew University of Jerusalem
**Year:** 2023

---

## Overview

`mri_unbias` is a MATLAB function for estimating and correcting intensity bias fields in 3D MRI images.
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
| `corrected_image` | Bias-corrected 3D image                                  |
| `bias_estimate`   | Estimated 3D bias field (same dimensions as input image) |

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

Outputs are saved in:

```
example_data/output/
```

---

## Example Output Files

| File                                        | Description                                     |
| ------------------------------------------- | ----------------------------------------------- |
| `t1_fl3d_FA30_unbiased_poly3.nii.gz`        | Corrected image                                 |
| `t1_fl3d_FA30_bias_estimation_poly3.nii.gz` | Estimated bias field                            |
| `before_after_visualization.png`            | Visualization comparing raw vs. corrected image |

---

## Notes

* The choice of polynomial degree (`poly_degree`) balances model smoothness and bias flexibility.
  Typical values are between 2–5.
* The method assumes that the masked tissue region (typically white matter) is approximately homogeneous in intensity.
  In practice, white matter exhibits biological variability, but this assumption provides a useful simplification for estimating the smooth bias field.

---

## Citation

If you use this function in your research, please cite:

> Drori, E., Mezer Lab, The Hebrew University of Jerusalem (2023).
> *MRI_UNBIAS: Polynomial bias field correction for MRI data.*


