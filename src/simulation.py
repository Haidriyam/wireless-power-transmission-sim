import math
from typing import Dict, Any


def calculate_quality_factor(inductance: float, resistance: float, frequency: float) -> float:
    """Calculate the unloaded quality factor (Q) of a resonance coil."""
    if resistance <= 0:
        raise ValueError("Coil resistance must be greater than zero.")
    omega = 2 * math.pi * frequency
    return (omega * inductance) / resistance


def calculate_coupling_coefficient(radius_tx: float, radius_rx: float, distance: float) -> float:
    """
    Estimate the magnetic coupling coefficient (k) between coaxial circular coils
    based on geometric dimensions and axial transfer distance.
    """
    if distance <= 0:
        return 1.0

    numerator = (radius_tx * radius_rx) ** 1.5
    denominator = (math.sqrt(radius_tx * radius_rx) ** 2 + distance ** 2) ** 1.5
    return min(1.0, numerator / denominator)


def evaluate_transmission_efficiency(
    k: float,
    q_tx: float,
    q_rx: float,
    figure_of_merit_load: float = 1.0
) -> Dict[str, Any]:
    """
    Compute theoretical wireless power transfer (WPT) efficiency.
    Efficiency equation: eta = (k^2 * Q_tx * Q_rx) / (1 + sqrt(1 + k^2 * Q_tx * Q_rx))^2
    """
    if k < 0 or k > 1:
        raise ValueError("Coupling coefficient k must be within [0, 1].")

    u = (k ** 2) * q_tx * q_rx

    efficiency = u / ((1 + math.sqrt(1 + u)) ** 2)

    return {
        "coupling_coefficient": round(k, 4),
        "figure_of_merit": round(u, 2),
        "efficiency_ratio": round(efficiency, 4),
        "efficiency_percentage": round(efficiency * 100, 2)
    }


if __name__ == "__main__":
    freq = 13.56e6
    l_tx, r_tx = 15e-6, 0.45
    l_rx, r_rx = 15e-6, 0.45

    q_1 = calculate_quality_factor(l_tx, r_tx, freq)
    q_2 = calculate_quality_factor(l_rx, r_rx, freq)

    dist = 0.15
    k_val = calculate_coupling_coefficient(0.1, 0.1, dist)
    report = evaluate_transmission_efficiency(k_val, q_1, q_2)

    print("\n[+] Wireless Power Transfer Simulation Results")
    print(f"    - Frequency: {freq / 1e6:.2f} MHz")
    print(f"    - Tx/Rx Quality Factor (Q): {q_1:.1f}")
    print(f"    - Coupling Coefficient (k): {report['coupling_coefficient']}")
    print(f"    - Theoretical Transfer Efficiency: {report['efficiency_percentage']}%\n")