from path import Path


def turbopath(input_path: str):
    """
    Normalize and convert a given input path to a normalized Path object.

    Args:
        input_path (str): The input path to be processed.

    Returns:
        Path: A Path object representing the normalized absolute path.
    """
    turbo_path = (
        Path(
            input_path,
        )
        .abspath()
        .normpath()
    )
    return turbo_path


def name_extractor(input_path: str):
    input_path = turbopath(input_path)
    file_name = input_path.name
    parts = file_name.split(".")
    return parts[0]
