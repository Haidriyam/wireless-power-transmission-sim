import unittest
from src.simulation import (
    calculate_quality_factor,
    calculate_coupling_coefficient,
    evaluate_transmission_efficiency
)


class TestWPTModel(unittest.TestCase):

    def test_quality_factor_calculation(self):
        q = calculate_quality_factor(10e-6, 1.0, 1e6)
        self.assertAlmostEqual(q, 62.83, places=1)

    def test_coupling_coefficient_limits(self):
        k_far = calculate_coupling_coefficient(0.05, 0.05, 5.0)
        self.assertLess(k_far, 0.01)

        k_zero = calculate_coupling_coefficient(0.05, 0.05, 0.0)
        self.assertEqual(k_zero, 1.0)

    def test_efficiency_output_bounds(self):
        result = evaluate_transmission_efficiency(k=0.15, q_tx=150, q_rx=150)
        self.assertIn("efficiency_percentage", result)
        self.assertGreaterEqual(result["efficiency_ratio"], 0.0)
        self.assertLessEqual(result["efficiency_ratio"], 1.0)


if __name__ == "__main__":
    unittest.main()