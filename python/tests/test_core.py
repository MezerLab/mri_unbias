import numpy as np
import pytest

from mri_unbias import (
    clip_bias_field_outside_mask,
    fit_bias_field,
    mri_unbias,
    polynomial_powers,
)


def test_polynomial_powers_total_degree():
    powers = polynomial_powers(2)

    assert (0, 0, 0) in powers
    assert (2, 0, 0) in powers
    assert (1, 1, 0) in powers
    assert (1, 1, 1) not in powers
    assert len(powers) == 10


def test_mri_unbias_recovers_known_linear_bias():
    shape = (9, 8, 7)
    x, y, z = np.meshgrid(
        np.linspace(-1.0, 1.0, shape[0]),
        np.linspace(-1.0, 1.0, shape[1]),
        np.linspace(-1.0, 1.0, shape[2]),
        indexing="ij",
    )
    bias = 2.0 + 0.2 * x - 0.1 * y + 0.05 * z
    image = 10.0 * bias
    mask = np.ones(shape, dtype=bool)

    corrected, estimated_bias = mri_unbias(image, mask, degree=1)

    np.testing.assert_allclose(estimated_bias, image, rtol=1e-12, atol=1e-12)
    np.testing.assert_allclose(corrected, np.ones(shape), rtol=1e-12, atol=1e-12)


def test_fit_bias_field_rejects_empty_finite_mask():
    image = np.full((2, 2, 2), np.nan)
    mask = np.ones((2, 2, 2), dtype=bool)

    with pytest.raises(ValueError, match="finite"):
        fit_bias_field(image, mask)


def test_mask_shape_must_match_image():
    image = np.ones((2, 2, 2))
    mask = np.ones((2, 2), dtype=bool)

    with pytest.raises(ValueError, match="mask shape"):
        mri_unbias(image, mask)


def test_brain_mask_clips_bias_only_outside_mask():
    image = np.ones((3, 3, 3))
    mask = np.ones((3, 3, 3), dtype=bool)
    brain_mask = np.zeros((3, 3, 3), dtype=bool)
    brain_mask[1, :, :] = True
    raw_bias = np.arange(27, dtype=float).reshape(3, 3, 3) - 10

    clipped = clip_bias_field_outside_mask(raw_bias, brain_mask)
    lower = raw_bias[brain_mask].min()
    upper = raw_bias[brain_mask].max()

    np.testing.assert_array_equal(clipped[brain_mask], raw_bias[brain_mask])
    assert clipped[~brain_mask].min() >= lower
    assert clipped[~brain_mask].max() <= upper

    corrected, applied_bias = mri_unbias(
        image,
        mask,
        degree=0,
        brain_mask=np.ones((3, 3, 3), dtype=bool),
    )
    np.testing.assert_allclose(applied_bias, np.ones((3, 3, 3)))
    np.testing.assert_allclose(corrected, np.ones((3, 3, 3)))
