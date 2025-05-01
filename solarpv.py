# ☀️ Run validations if executed directly

class SolarPV:
    """
    The SolarPV class models a grid-connected solar PV generator.
    It injects real power (P) and maintains constant voltage magnitude like a PV bus.
    """

    def __init__(self, name: str, bus, rated_power: float, voltage_setpoint: float = 1.0):
        """
        Initializes the SolarPV generator with name, associated bus, rated power, and voltage setpoint.

        :param name: Unique name of the solar PV unit
        :param bus: The bus object this PV is connected to
        :param rated_power: Real power output in MW (must be non-negative)
        :param voltage_setpoint: Desired voltage magnitude in per unit (default 1.0)
        """
        self.name = name
        self.bus = bus
        self.rated_power = rated_power
        self.capacity_mw = rated_power  # Alias for compatibility with circuit summaries
        self.voltage_setpoint = voltage_setpoint
        self.validate()  # Ensure parameters are within valid range

    def validate(self):
        """
        Validates that rated power is non-negative and voltage setpoint is within 0.9 to 1.1 pu.
        Raises ValueError if invalid input is detected.
        """
        if self.rated_power < 0:
            raise ValueError(f"Rated power for {self.name} must be non-negative.")
        if not (0.9 <= self.voltage_setpoint <= 1.1):
            raise ValueError(f"Voltage setpoint for {self.name} must be within [0.9, 1.1] p.u.")

    def inject_power(self):
        """
        Injects real power (in per unit) into the connected bus and sets its voltage magnitude.
        Assumes system base MVA of 100 for per-unit conversion.
        """
        self.bus.P_spec += self.rated_power / 100  # Convert MW to per unit
        self.bus.vpu = self.voltage_setpoint       # Set bus voltage

    def get_pu_generation(self, system_base_mva=100.0):
        """
        Returns the real power output in per unit based on a given system base MVA.
        """
        return self.rated_power / system_base_mva


# ✅ Testing the SolarPV class
if __name__ == '__main__':
    # Define a mock bus class for testing
    class DummyBus:
        def __init__(self, name):
            self.name = name
            self.P_spec = 0.0  # Real power specification in pu
            self.vpu = 1.0     # Voltage magnitude in pu

    print("Running SolarPV validation tests...\n")

    # ✅ TEST 1: Valid PV unit with 50 MW at 1.0 pu voltage
    try:
        bus = DummyBus("Bus A")
        pv = SolarPV("PV1", bus, rated_power=50, voltage_setpoint=1.0)
        pv.inject_power()
        print(f"{pv.name} successfully injected {pv.rated_power} MW at {pv.voltage_setpoint} p.u. to {pv.bus.name}")
    except ValueError as e:
        print("Failed valid PV test:", e)

    # ✅ TEST 2: Valid PV with 10 MW at 0.95 pu voltage
    try:
        bus = DummyBus("Bus D")
        pv = SolarPV("PV4", bus, rated_power=10, voltage_setpoint=0.95)
        pv.inject_power()
        print(f"{pv.name} successfully injected {pv.rated_power} MW at {pv.voltage_setpoint} p.u. to {pv.bus.name}")
    except ValueError as e:
        print("Failed second valid PV test:", e)

    # ✅ TEST 3: Valid PV with 25 MW at upper voltage limit of 1.08 pu
    try:
        bus = DummyBus("Bus E")
        pv = SolarPV("PV5", bus, rated_power=25, voltage_setpoint=1.08)
        pv.inject_power()
        print(f"{pv.name} successfully injected {pv.rated_power} MW at {pv.voltage_setpoint} p.u. to {pv.bus.name}")
    except ValueError as e:
        print("Failed third valid PV test:", e)

    # ❌ TEST 4: Negative power should raise an error
    try:
        bus = DummyBus("Bus B")
        SolarPV("PV2", bus, rated_power=-20, voltage_setpoint=1.0)
        print("Error: Negative power test did not raise")
    except ValueError as e:
        print("Correctly caught invalid power:", e)

    # ❌ TEST 5: Voltage too high (1.2 pu) should raise an error
    try:
        bus = DummyBus("Bus C")
        SolarPV("PV3", bus, rated_power=30, voltage_setpoint=1.2)
        print("Error: Out-of-range voltage test did not raise")
    except ValueError as e:
        print("Correctly caught invalid voltage:", e)

