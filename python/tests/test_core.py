import numpy as np
import pytest

from mri_unbias import fit_bias_field, mri_unbias, polynomial_powers


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
