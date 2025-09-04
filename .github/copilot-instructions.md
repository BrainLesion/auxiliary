# auxiliary - Medical Image Processing Utilities

auxiliary is a Python package that provides utilities for medical image processing, including NIfTI I/O, DICOM conversion, image normalization, TIFF processing, and script execution utilities. The package is built with Poetry and designed for research in brain lesion analysis.

**Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Essential Setup Commands
Run these commands in sequence to set up the development environment:

```bash
# Install Poetry (if not available)
pip install poetry

# Install all dependencies - NEVER CANCEL: Takes 10-15 seconds, includes NumPy compilation
# Set timeout to 60+ seconds to be safe
export PATH=$PATH:~/.local/bin
poetry install

# Install with optional dcm2niix functionality (for DICOM conversion)
poetry install --extras dcm2niix

# Install documentation dependencies
poetry install --with docs
```

### Building and Testing

```bash
# Build the package - NEVER CANCEL: Takes 3-5 seconds
# Set timeout to 30+ seconds  
poetry build

# Test basic functionality (manual validation since no unit tests exist)
poetry run python -c "
import auxiliary.io as aio
import numpy as np
import tempfile
import os

# Create test data and verify I/O works
test_array = np.random.rand(10, 10, 10).astype(np.float32)
with tempfile.NamedTemporaryFile(suffix='.nii.gz', delete=False) as tmp:
    aio.write_image(test_array, tmp.name)
    loaded = aio.read_image(tmp.name)
    assert np.allclose(test_array, loaded)
    os.unlink(tmp.name)
print('✅ Basic I/O functionality test PASSED')
"

# Build documentation - NEVER CANCEL: Takes 1-10 seconds depending on cache
# Set timeout to 60+ seconds
cd docs
poetry run make html
cd ..
```

### Code Quality and Linting

```bash
# Format code with black (used by CI)
pip install black  # Install globally if not in Poetry
black --check --verbose .

# To auto-format (what CI does):
black .

# Validate import structure
poetry run python -c "
import auxiliary.io
import auxiliary.conversion  
import auxiliary.runscript
import auxiliary.nifti
import auxiliary.normalization
import auxiliary.tiff
import auxiliary.turbopath
print('✅ All modules import successfully')
"
```

## Validation Scenarios

**CRITICAL**: Always run these complete validation scenarios after making changes to ensure functionality:

### 1. Image I/O Validation
```bash
# Test NIfTI image reading/writing with SimpleITK backend
poetry run python -c "
import auxiliary.io as aio
import numpy as np
import tempfile
import os

# Test different data types and shapes
for dtype in [np.float32, np.int16, np.uint8]:
    for shape in [(64, 64, 32), (128, 128), (10, 10, 10, 5)]:
        test_data = np.random.rand(*shape).astype(dtype)
        with tempfile.NamedTemporaryFile(suffix='.nii.gz', delete=False) as tmp:
            try:
                aio.write_image(test_data, tmp.name)
                loaded = aio.read_image(tmp.name)
                assert loaded.shape == test_data.shape
                assert loaded.dtype == test_data.dtype
                print(f'✅ {dtype} {shape} - OK')
            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)
print('✅ Complete I/O validation PASSED')
"
```

### 2. DICOM Conversion Validation (if dcm2niix installed)
```bash
# Test dcm2niix availability
poetry run dcm2niix -h | head -5

# Test conversion module import
poetry run python -c "
import auxiliary.conversion as conv
print('Available functions:', [x for x in dir(conv) if not x.startswith('_')])
print('✅ DICOM conversion module available')
"
```

### 3. Script Runner Validation
```bash
# Test script execution utilities
poetry run python -c "
import auxiliary.runscript as rs
runner = rs.ScriptRunner('/bin/echo', '/tmp/test.log')
success, output = runner.run(['Hello', 'World'])
print(f'Script runner test: success={success}')
print('✅ Script runner validation PASSED')
"
```

## Common Tasks and Timing Expectations

### Installation Timing
- **Poetry install**: 10-15 seconds (includes NumPy compilation)
- **Poetry install --extras dcm2niix**: +3-5 seconds for dcm2niix
- **Poetry install --with docs**: +30-45 seconds for Sphinx dependencies

### Build Timing
- **Poetry build**: 3-5 seconds
- **Documentation build**: 1-10 seconds (depends on cache)
- **Black formatting check**: 1-2 seconds

### NEVER CANCEL Commands
- Set timeout to **60+ seconds** for `poetry install` commands
- Set timeout to **30+ seconds** for `poetry build`  
- Set timeout to **60+ seconds** for documentation builds

## Repository Structure

```
.
├── auxiliary/              # Main Python package
│   ├── io.py              # Image I/O utilities (SimpleITK)
│   ├── conversion.py      # DICOM/NIfTI conversion  
│   ├── runscript.py       # Script execution utilities
│   ├── nifti/             # NIfTI-specific utilities
│   ├── normalization/     # Image normalization functions
│   ├── tiff/              # TIFF processing utilities
│   └── turbopath/         # Path manipulation utilities
├── docs/                  # Sphinx documentation
├── pyproject.toml         # Poetry configuration and dependencies
├── .github/workflows/     # CI/CD pipelines
└── README.md
```

## CI/CD Pipeline Requirements

The repository uses GitHub Actions with reusable workflows from BrainLesion/BrainLes:

```bash
# Before committing, always run:
black --check .  # Must pass or CI will fail

# The CI will:
# 1. Check code formatting with black
# 2. Auto-format on comment '/format' in PRs  
# 3. Release to PyPI on GitHub releases
```

## Key Dependencies and Their Purposes

- **numpy**: Core array operations and medical image data
- **SimpleITK**: Medical image I/O (NIfTI, DICOM, etc.)
- **tifffile**: TIFF image processing
- **pillow**: General image processing support
- **loguru**: Structured logging
- **dcm2niix** (optional): High-performance DICOM to NIfTI conversion
- **pytest**: Testing framework (no tests currently exist)

## Troubleshooting

### Poetry Issues
```bash
# If Poetry is not found:
export PATH=$PATH:~/.local/bin

# If build fails with "poetry.dev-dependencies deprecated":
# This is just a warning, ignore it. The build will work.

# If standard 'python -m build' fails:
# Use 'poetry build' instead - it works reliably.
```

### Import Issues
```bash
# Test all imports work:
poetry run python -c "
modules = ['io', 'conversion', 'runscript', 'nifti', 'normalization', 'tiff', 'turbopath']
for mod in modules:
    exec(f'import auxiliary.{mod}')
    print(f'✅ auxiliary.{mod}')
"
```

### No Tests Exist
This repository currently has no unit tests (`pytest` collects 0 items). Validation must be done manually using the validation scenarios above. Always run the complete validation scenarios after making changes.

## Working with the Codebase

- **Main I/O**: Use `auxiliary.io.write_image()` and `auxiliary.io.read_image()` for medical images
- **DICOM conversion**: Use `auxiliary.conversion.dcm2niix()` or related functions
- **Script execution**: Use `auxiliary.runscript.ScriptRunner` for running external tools
- **Documentation**: Built with Sphinx, uses MyST parser for Markdown support
- **Code style**: Must pass `black --check .` for CI to pass

Always test functionality manually with real data after making changes since automated tests do not exist.