# --- solar.py ---
import numpy as np


class Solar:
    """
    A class to model a solar PV array's real power output using HOMER's output equation.
    """

    def __init__(self, name, bus, rated_capacity_kw, derate_factor,
                 G_t, G_stc, alpha_p, T_c, T_stc=25):
        """
        Initialize the Solar object.

        Parameters:
        - name (str): Identifier for the solar unit.
        - bus (Bus): The bus object the PV unit is connected to.
        - rated_capacity_kw (float): PV array output under STC [kW].
        - derate_factor (float): Derating factor [% as decimal].
        - G_t (float): Current radiation incident on the PV [kW/m²].
        - G_stc (float): Radiation at STC [1.0 kW/m²].
        - alpha_p (float): Temperature coefficient of power [%/°C as decimal].
        - T_c (float): PV cell temperature at current step [°C].
        - T_stc (float): PV cell temp under STC [25°C by default].
        """
        self.name = name
        self.bus = bus
        self.rated_capacity_kw = rated_capacity_kw
        self.derate_factor = derate_factor
        self.G_t = G_t
        self.G_stc = G_stc
        self.alpha_p = alpha_p
        self.T_c = T_c
        self.T_stc = T_stc

    def calc_power_output(self) -> float:
        """
        Calculate real power output from the PV array [kW].

        Returns:
        - float: Real power output [kW]
        """
        temp_effect = 1 + self.alpha_p * (self.T_c - self.T_stc)
        return self.rated_capacity_kw * self.derate_factor * (self.G_t / self.G_stc) * temp_effect

    def __str__(self):
        return f"SolarPV(name={self.name}, bus={self.bus.name}, rated_capacity={self.rated_capacity_kw} kW)"



# Testing

if __name__ == '__main__':
    print("=== SolarPV Class: Validation Testing ===")


    class MockBus:
        """Minimal Bus mock for unit testing."""

        def __init__(self, name):
            self.name = name


    # Test Cases
    test_cases = [
        {
            "description": "STC conditions",
            "params": {
                "rated_capacity_kw": 100,
                "derate_factor": 1.0,
                "G_t": 1.0,
                "G_stc": 1.0,
                "alpha_p": 0.0,
                "T_c": 25
            },
            "expected": 100.0
        },
        {
            "description": "Normal use with derate & mild temp loss",
            "params": {
                "rated_capacity_kw": 100,
                "derate_factor": 0.9,
                "G_t": 0.85,
                "G_stc": 1.0,
                "alpha_p": -0.004,
                "T_c": 35
            },
            "expected": 100 * 0.9 * 0.85 * (1 + (-0.004) * (35 - 25))  # ≈ 74.97 kW
        },
        {
            "description": "Hot day edge case",
            "params": {
                "rated_capacity_kw": 100,
                "derate_factor": 1.0,
                "G_t": 1.0,
                "G_stc": 1.0,
                "alpha_p": -0.0045,
                "T_c": 60
            },
            "expected": 100 * (1 + (-0.0045) * (60 - 25))  # ≈ 84.25 kW
        }
    ]

    for i, case in enumerate(test_cases, 1):
        bus = MockBus("Bus 1")
        pv = Solar(f"TestPV{i}", bus, **case["params"])
        result = pv.calc_power_output()
        expected = case["expected"]
        print(f"\nTest {i}: {case['description']}")
        print(f"  Expected Output ≈ {expected:.2f} kW")
        print(f"  Calculated Output = {result:.2f} kW")
        assert np.isclose(result, expected, atol=0.5), "❌ Test failed: Output mismatch"

    print("\n✅ All SolarPV validation tests passed successfully.")
