import numpy as np


def roll(array: np.ndarray, shift: int) -> np.ndarray:
    """Roll array along first axis, replacing wrapped entries with NaN."""
    result = np.roll(array, shift)
    if shift > 0:
        result[:shift] = np.nan
    elif shift < 0:
        result[shift:] = np.nan
    return result
