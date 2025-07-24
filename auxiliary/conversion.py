import subprocess
import time
from pathlib import Path
from typing import Optional, Union

import numpy as np
import SimpleITK as sitk
from loguru import logger
from numpy.typing import NDArray


def dcm2niix(
    input_dir: Union[Path, str],
    output_dir: Union[Path, str],
    file_name: Optional[str] = None,
    compress: bool = True,
) -> None:
    """
    Convert a DICOM series to NIfTI format using dcm2niix.

    Args:
        input_dir (Union[Path, str]): Path to the input DICOM directory.
        output_dir (Union[Path, str]): Path to the output NIfTI directory.
        file_name (Optional[str], optional): Custom naming for the output NIfTI file. For details refer to `dcm2niix -f` option documentation (https://github.com/rordenlab/dcm2niix). Defaults to None.
        compress (bool, optional): Whether to gz compress the output NIfTI file. Defaults to True.

    Raises:
        RuntimeError: If the input directory is not valid or if the conversion fails.
        RuntimeError: If the dcm2niix command fails.
    """

    # Ensure Path objects
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    if not input_dir.exists() or not input_dir.is_dir():
        raise RuntimeError(f"{input_dir} is not a valid directory.")
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = ["dcm2niix"]

    # Add filename pattern early (must come before input path)
    if file_name:
        cmd += ["-f", file_name]

    # Add output options
    cmd += [
        "-o",
        str(output_dir),
        "-z",
        "y" if compress else "n",
        str(input_dir),  # always last
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to convert DICOM to NIfTI using dcm2niix: {e}")
        raise RuntimeError(
            f"Failed to convert DICOM to NIfTI using dcm2niix: {e}; please try `dicom_to_nifti_itk`"
        ) from e


def dicom_to_nifti_itk(
    input_dir: Union[Path, str],
    output_dir: Union[Path, str],
    file_name: Optional[str] = None,
) -> None:
    """
    Convert a DICOM series to NIfTI format using SimpleITK.
    Args:
        input_dir (Union[Path, str]): Path to the input DICOM directory.
        output_dir (Union[Path, str]): Path to the output NIfTI directory.
        file_name (Optional[str], optional): Name of the output NIfTI file if there is only one DICOM series to be converted. Defaults to None.

    Raises:
        RuntimeError: If the input directory is not valid or does not contain a DICOM series.
    """

    # Ensure Path objects
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    if not input_dir.exists() or not input_dir.is_dir():
        raise RuntimeError(f"{input_dir} is not a valid directory.")

    # create the folder output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    series_IDs = sitk.ImageSeriesReader.GetGDCMSeriesIDs(str(input_dir))
    if not series_IDs:
        raise RuntimeError(f"{input_dir} does not contain a valid DICOM series.")

    if len(series_IDs) > 1:
        logger.warning(f"More than 1 DICOM series was found in the folder: {input_dir}")

    for series_id in series_IDs:
        series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(
            input_dir, series_id
        )
        series_reader = sitk.ImageSeriesReader()
        series_reader.SetFileNames(series_file_names)
        series_reader.MetaDataDictionaryArrayUpdateOn()
        series_reader.LoadPrivateTagsOn()
        image_dicom = series_reader.Execute()

        output_path = output_dir / f"{series_id}.nii.gz"

        if file_name:
            if len(series_IDs) > 1:
                logger.warning(
                    f"More than 1 DICOM series was found in the folder: {input_dir}. Ignoring the provided file name ({file_name}) and using the series ID ({series_id}) instead."
                )
            else:
                output_path = output_dir / file_name

        sitk.WriteImage(
            image_dicom,
            output_path,
        )


def nifti_to_dicom_itk(
    input_image: Union[Path, str, sitk.Image, NDArray],
    output_dir: Union[Path, str],
    reference_dicom: Optional[Union[Path, str]] = None,
):
    """
    Convert a NIfTI image to DICOM format using SimpleITK.

    Args:
        input_image (Union[Path, str, sitk.Image, NDArray]): Path to the input NIfTI image or a SimpleITK image or numpy array.
        output_dir (Union[Path, str]): Path to the output DICOM directory.
        reference_dicom (Optional[Union[Path, str]], optional): Path to a reference DICOM file or directory for metadata. Defaults to None.

    Raises:
        RuntimeError: If no DICOM series is found in the reference directory.
        TypeError: If input_image is not a valid type (file path, SimpleITK.Image, or np.ndarray).
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load or convert input to SimpleITK.Image
    if isinstance(input_image, (str, Path)):
        image = sitk.ReadImage(str(input_image))
    elif isinstance(input_image, sitk.Image):
        image = input_image
    elif isinstance(input_image, np.ndarray):
        image = sitk.GetImageFromArray(input_image)
    else:
        raise TypeError(
            "input_image must be a file path, SimpleITK.Image, or np.ndarray"
        )

    # Write to DICOM
    writer = sitk.ImageFileWriter()
    tags_to_copy = [
        # "0010|0010",  # Patient Name
        "0010|0020",  # Patient ID
        "0010|0030",  # Patient Birth Date
        "0020|000D",  # Study Instance UID, for machine consumption
        "0020|0010",  # Study ID, for human consumption
        "0008|0020",  # Study Date
        "0008|0030",  # Study Time
        "0008|0050",  # Accession Number
        "0008|0060",  # Modality
    ]

    # Use the study/series/frame of reference information given in the meta-data
    # dictionary and not the automatically generated information from the file IO
    writer.KeepOriginalImageUIDOn()
    modification_time = time.strftime("%H%M%S")
    modification_date = time.strftime("%Y%m%d")
    direction = image.GetDirection()

    if reference_dicom:
        reference_dicom_path = Path(reference_dicom)
        if reference_dicom_path.is_dir():

            series_ids = sitk.ImageSeriesReader.GetGDCMSeriesIDs(str(reference_dicom))
            if not series_ids:
                raise RuntimeError(f"No DICOM series found in: {reference_dicom}")
            if len(series_ids) > 1:
                logger.warning(
                    f"More than 1 DICOM series was found in the folder: {reference_dicom}. Using the first one ({series_ids[0]}) as reference."
                )
            # Pick the first series by default
            dicom_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(
                str(reference_dicom), series_ids[0]
            )

            reader = sitk.ImageSeriesReader()
            reader.SetFileNames(dicom_names)
            reader.MetaDataDictionaryArrayUpdateOn()
            reader.Execute()

            series_tag_values = [
                (k, reader.GetMetaData(0, k.lower()))
                for k in tags_to_copy
                if reader.HasMetaDataKey(0, k.lower())
            ]
        elif reference_dicom_path.is_file():
            image_ref = sitk.ReadImage(str(reference_dicom))
            series_tag_values = [
                (k, image_ref.GetMetaData(k.lower()))
                for k in tags_to_copy
                if image_ref.HasMetaDataKey(k.lower())
            ]
        else:
            raise RuntimeError(
                f"{reference_dicom} is not a valid DICOM file or directory."
            )
    else:
        series_tag_values = []

    series_tag_values.extend(
        [
            ("0008|0031", modification_time),  # Series Time
            ("0008|0021", modification_date),  # Series Date
            ("0008|0008", "DERIVED\\SECONDARY"),  # Image Type
            (
                "0020|000e",
                "1.2.826.0.1.3680043.2.1125."
                + modification_date
                + ".1"
                + modification_time,
            ),
            # Series Instance UID
            (
                "0020|0037",
                "\\".join(
                    map(
                        str,
                        (
                            direction[0],
                            direction[3],
                            direction[6],
                            direction[1],
                            direction[4],
                            direction[7],
                        ),  # Image Orientation (Patient)
                    )
                ),
            ),
        ]
    )

    try:
        for i in range(image.GetDepth()):
            image_slice = image[:, :, i]
            # Tags shared by the series.
            for tag, value in series_tag_values:
                image_slice.SetMetaData(tag, value)
            # Slice specific tags.
            #   Instance Creation Date
            image_slice.SetMetaData("0008|0012", modification_time)
            #   Instance Creation Time
            image_slice.SetMetaData("0008|0013", modification_date)
            #   Image Position (Patient)
            image_slice.SetMetaData(
                "0020|0032",
                "\\".join(map(str, image.TransformIndexToPhysicalPoint((0, 0, i)))),
            )
            #   Instance Number
            image_slice.SetMetaData("0020|0013", str(i))

            # Write to the output directory and add the extension dcm, to force writing in DICOM format.
            writer.SetFileName(output_dir / f"{i}.dcm")
            writer.Execute(image_slice)
    except Exception as e:
        logger.error(f"Could not write DICOM image: {e}")
