conversion
============================================

The conversion module provides utilities for converting between DICOM and NIfTI formats.

DICOM to NIfTI Conversion
--------------------------

dcm2niix
~~~~~~~~~

.. autofunction:: auxiliary.conversion.dcm2niix

dicom_to_nifti_itk
~~~~~~~~~~~~~~~~~~

.. autofunction:: auxiliary.conversion.dicom_to_nifti_itk

NIfTI to DICOM Conversion
--------------------------

nifti_to_dicom_itk
~~~~~~~~~~~~~~~~~~

.. autofunction:: auxiliary.conversion.nifti_to_dicom_itk

Examples
--------

Converting DICOM to NIfTI using dcm2niix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from auxiliary.conversion import dcm2niix
    
    # Convert DICOM series to compressed NIfTI
    dcm2niix(
        input_dir="/path/to/dicom/series",
        output_dir="/path/to/output",
        file_name="my_image",
        compress=True
    )

Converting DICOM to NIfTI using SimpleITK
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from auxiliary.conversion import dicom_to_nifti_itk
    
    # Convert DICOM series to NIfTI using SimpleITK
    dicom_to_nifti_itk(
        input_dir="/path/to/dicom/series",
        output_dir="/path/to/output",
        file_name="my_image.nii.gz"
    )

Converting NIfTI to DICOM
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from auxiliary.conversion import nifti_to_dicom_itk
    
    # Convert NIfTI image to DICOM series
    nifti_to_dicom_itk(
        input_image="/path/to/image.nii.gz",
        output_dir="/path/to/dicom/output",
        reference_dicom="/path/to/reference/dicom"
    )
    
    # You can also pass numpy arrays or SimpleITK images
    import numpy as np
    image_array = np.random.rand(100, 100, 50)
    nifti_to_dicom_itk(
        input_image=image_array,
        output_dir="/path/to/dicom/output"
    )