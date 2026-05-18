"""Command-line interface for mri-unbias."""

from __future__ import annotations

import argparse

from .io import unbias_nifti


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Polynomial MRI bias-field correction")
    parser.add_argument("image", help="Input 3D NIfTI image")
    parser.add_argument("mask", help="Binary homogeneous-region mask NIfTI")
    parser.add_argument("--degree", type=int, default=3, help="Polynomial degree")
    parser.add_argument("--corrected", required=True, help="Output corrected NIfTI path")
    parser.add_argument("--bias-field", required=True, help="Output bias-field NIfTI path")
    args = parser.parse_args(argv)

    corrected_path, bias_field_path = unbias_nifti(
        args.image,
        args.mask,
        args.corrected,
        args.bias_field,
        degree=args.degree,
    )
    print(f"Wrote corrected image: {corrected_path}")
    print(f"Wrote bias field: {bias_field_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
