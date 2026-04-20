import numpy as np


def scale_position(
    position: int,
) -> float:
    """Scale the position of the car to a value between 0 and 1.

    Args:
        position (int): The position of the car

    Returns:
        float: The scaled position of the car
    """
    return (position - 1) / 19

def inverse_scale_position(
    scaled_position: float,
) -> int:
    """Inverse scale the position of the car to a value between 1 and 20.

    Args:
        scaled_position (float): The scaled position of the car

    Returns:
        int: The position of the car
    """
    return int(scaled_position * 19 + 1)

def scale_stint_length(
    stint_length: int,
) -> float:
    """Scale the stint length to a value between 0 and 1.

    Args:
        stint_length (int): The stint length

    Returns:
        float: The scaled stint length
    """
    return 1 / 100 * stint_length

def inverse_scale_stint_length(
    scaled_stint_length: float,
) -> int:
    """Inverse scale the stint length to a value between 1 and 100.

    Args:
        scaled_stint_length (float): The scaled stint length

    Returns:
        int: The stint length
    """
    return int(scaled_stint_length * 100)

def scale_gap_ahead(
    gap_ahead: float,
) -> float:
    """Scale the gap to a value between -1 and 1.
    (30 -> 1), (-30 -> -1)

    Args:
        gap (float): The gap ahead to scale

    Returns:
        float: The scaled gap ahead
    """
    if gap_ahead > 30:
        return 1
    elif gap_ahead < -30:
        return -1
    return (1 / 30) * gap_ahead

def inverse_scale_gap_ahead(
    scaled_gap_ahead: float,
) -> float:
    """Inverse scale the gap to a value between -30 and 30.

    Args:
        scaled_gap_ahead (float): The scaled gap ahead

    Returns:
        float: The gap ahead
    """
    return scaled_gap_ahead * 30

def scale_gap_behind(
    gap_behind: float,
) -> float:
    """Scale the gap behind to a value between -1 and 1.
    (30 -> 1), (-30 -> -1)

    Args:
        gap_behind (float): The gap behind to scale

    Returns:
        float: The scaled gap behind
    """
    if gap_behind < -30:
        return -1
    elif gap_behind > 30:
        return 1
    return (1 / 30) * gap_behind

def inverse_scale_gap_behind(
    scaled_gap_behind: float,
) -> float:
    """Inverse scale the gap to a value between -30 and 30.

    Args:
        scaled_gap_behind (float): The scaled gap behind

    Returns:
        float: The gap behind
    """
    return scaled_gap_behind * 30

def scale_gap_to_leader(
    gap_to_leader: float,
) -> float:
    """Scale the gap to leader to a value between -1 and 1.
    (-30 -> -1), (200 -> 1)
    Args:
        gap_to_leader (float): The gap to scale

    Returns:
        float: The scaled gap
    """
    if gap_to_leader > 200:
        return 1
    elif gap_to_leader < -30:
        return -1
    return (1 / 115) * gap_to_leader - (17 / 23)

def inverse_scale_gap_to_leader(
    scaled_gap_to_leader: float,
) -> float:
    """Inverse scale the gap to a value between -30 and 200.

    Args:
        scaled_gap_to_leader (float): The scaled gap

    Returns:
        float: The gap
    """
    return (scaled_gap_to_leader + (17 / 23)) * 115

def scale_tyre_degradation(
    tyre_degradation: float,
) -> float:
    """Scale the tyre degradation to a value between 0 and 1.

    Args:
        tyre_degradation (int): The tyre degradation

    Returns:
        float: The scaled tyre degradation
    """
    return 1 if tyre_degradation > 20 else tyre_degradation / 20

def inverse_scale_tyre_degradation(
    scaled_tyre_degradation: float,
) -> float:
    """Inverse scale the tyre degradation to a value between 0 and 20.

    Args:
        scaled_tyre_degradation (float): The scaled tyre degradation

    Returns:
        float: The tyre degradation
    """
    return scaled_tyre_degradation * 20

def scale_last_lap_to_reference(
    last_lap_to_reference: float,
) -> float:
    """Scale the last lap time to a value between 0 and 1.

    Args:
        last_lap_to_reference (float): The last lap time

    Returns:
        float: The scaled last lap time
    """
    return np.log(last_lap_to_reference)

def inverse_scale_last_lap_to_reference(
    scaled_last_lap_to_reference: float,
) -> float:
    """Inverse scale the last lap time to a value between 0 and 1.

    Args:
        scaled_last_lap_to_reference (float): The scaled last lap time

    Returns:
        float: The last lap time
    """
    return np.exp(scaled_last_lap_to_reference)