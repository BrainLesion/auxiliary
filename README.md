# auxiliary

[![Python Versions](https://img.shields.io/pypi/pyversions/auxiliary)](https://pypi.org/project/auxiliary/)
[![Stable Version](https://img.shields.io/pypi/v/auxiliary?label=stable)](https://pypi.org/project/auxiliary/)
[![Documentation Status](https://readthedocs.org/projects/auxiliary/badge/?version=latest)](http://auxiliary.readthedocs.io/?badge=latest)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Auxiliary is a Python package providing utility functions for medical image processing. It is part of the [BrainLesion](https://github.com/BrainLesion) project and offers tools for:

- **Image I/O**: Reading and writing medical images (NIfTI, TIFF, DICOM) using SimpleITK
- **Image Normalization**: Percentile-based and windowing normalization methods
- **Format Conversion**: DICOM to NIfTI and NIfTI to DICOM conversion
- **Path Utilities**: Robust path handling with the turbopath module

## Installation

With a Python 3.10+ environment, you can install `auxiliary` directly from [PyPI](https://pypi.org/project/auxiliary/):

```bash
pip install auxiliary
```

Or via conda:

```bash
conda install conda-forge::auxiliary
```

### Optional Dependencies

For DICOM to NIfTI conversion using `dcm2niix`:

```bash
pip install auxiliary[dcm2niix]
```

## Usage

### NIfTI I/O

```python
from auxiliary.io import read_image, write_image

# Read a NIfTI image
image_array = read_image("path/to/image.nii.gz")

# Write a NumPy array to a NIfTI file
write_image(image_array, "path/to/output.nii.gz")

# Write with reference image for spatial metadata
write_image(image_array, "path/to/output.nii.gz", reference_path="path/to/reference.nii.gz")
```

### DICOM I/O

```python
from auxiliary.conversion import dicom_to_nifti_itk, nifti_to_dicom_itk, dcm2niix

# Read a DICOM series and convert to NIfTI using SimpleITK
dicom_to_nifti_itk("path/to/dicom_dir", "path/to/output_dir")

# Read a DICOM series and convert to NIfTI using dcm2niix (requires dcm2niix extra)
dcm2niix("path/to/dicom_dir", "path/to/output_dir")

# Write a NIfTI image to DICOM format
nifti_to_dicom_itk("path/to/image.nii.gz", "path/to/output_dicom_dir")

# Write with reference DICOM for metadata
nifti_to_dicom_itk(
    "path/to/image.nii.gz",
    "path/to/output_dicom_dir",
    reference_dicom="path/to/reference_dicom_dir"
)
```

### TIFF I/O

```python
from auxiliary.tiff.io import read_tiff, write_tiff

# Read a TIFF file
tiff_data = read_tiff("path/to/image.tiff")

# Write a NumPy array to a TIFF file
write_tiff(tiff_data, "path/to/output.tiff")
```

### Image Normalization

```python
from auxiliary.normalization.percentile_normalizer import PercentileNormalizer
from auxiliary.normalization.windowing_normalizer import WindowingNormalizer

# Percentile-based normalization
normalizer = PercentileNormalizer(lower_percentile=1.0, upper_percentile=99.0)
normalized_image = normalizer.normalize(image_array)

# Windowing normalization (e.g., for CT images)
normalizer = WindowingNormalizer(center=40, width=400)
windowed_image = normalizer.normalize(image_array)
```
