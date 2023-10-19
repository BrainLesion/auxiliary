# Is this needed?

from .percentile_normalizer import PercentileNormalizer
from .windowing_normalizer import WindowingNormalizer

import numpy as np


def normalize_with_percentiles(
    image: np.ndarray,
    lower_percentile: float = 0.0,
    upper_percentile: float = 100.0,
    lower_limit: float = 0,
    upper_limit: float = 1,
):
    """
    Normalize an input image using percentile-based normalization.

    Parameters:
        image (numpy.ndarray): The input image.
        lower_percentile (float): The lower percentile for mapping.
        upper_percentile (float): The upper percentile for mapping.
        lower_limit (float): The lower limit for normalized values.
        upper_limit (float): The upper limit for normalized values.

    Returns:
        numpy.ndarray: The normalized image.
    """
    # Create an instance of the PercentileNormalizer class
    normalizer = PercentileNormalizer(
        lower_percentile, upper_percentile, lower_limit, upper_limit
    )

    # Call the normalize method of the normalizer instance
    normalized_image = normalizer.normalize(image)

    return normalized_image


def normalize_with_windowing(
    image: np.ndarray,
    center: float,
    width: float,
):
    """
    Normalize an input image using windowing-based normalization.

    Parameters:
        image (numpy.ndarray): The input image.
        center (float): The window center.
        width (float): The window width.

    Returns:
        numpy.ndarray: The normalized image.
    """
    # Create an instance of the WindowingNormalizer class
    normalizer = WindowingNormalizer(center, width)

    # Call the normalize method of the normalizer instance
    normalized_image = normalizer.normalize(image)

    return normalized_image
