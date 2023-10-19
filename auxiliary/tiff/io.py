from tifffile import imread, imwrite
import os
from pathlib import Path


# Why not use imread directly?
def read_tiff(tiff_path: str):
    data = imread(tiff_path)
    return data


def write_tiff(
    numpy_array,
    output_tiff_path: str,
    create_parent_directory: bool = False,
    transpose: bool = False,
):
    if transpose:
        numpy_array = numpy_array.T

    output_path = Path(output_tiff_path).resolve()
    if create_parent_directory:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
    imwrite(output_path, numpy_array)
