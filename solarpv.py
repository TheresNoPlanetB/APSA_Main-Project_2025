class SolarPV:
    """
    The SolarPV class models a grid-connected solar PV generator.
    It injects real power (P) and maintains constant voltage magnitude like a PV bus.
    """

    def __init__(self, name: str, bus, rated_power: float, voltage_setpoint: float = 1.0):
        """
        Initialize the SolarPV generator.

        :param name: Name of the solar PV unit
        :param bus: Associated bus object
        :param rated_power: Rated power output in MW
        :param voltage_setpoint: Voltage setpoint in per unit (default 1.0)
        """
        self.name = name
        self.bus = bus
        self.rated_power = rated_power
        self.voltage_setpoint = voltage_setpoint

    def inject_power(self):
        """
        Apply power injection to the bus. Acts as a PV generator.
        """
        self.bus.P_spec += self.rated_power / 100  # convert to per unit on 100 MVA base
        self.bus.vpu = self.voltage_setpoint

    def get_pu_generation(self, system_base_mva=100.0):
        """
        Return power output in per unit based on the system base MVA.
        """
        return self.rated_power / system_base_mva


if __name__ == "__main__":
    from bus import Bus  # 🟡 Import your Bus class to test integration

    # 🌞 Create a dummy bus to attach the solar PV
    test_bus = Bus(name="Test Bus", base_kv=12.47, bus_type="PV Bus")

    # 🌞 Instantiate a SolarPV unit
    solar_unit = SolarPV(name="Solar_Unit_1", bus=test_bus, rated_power=5.0, voltage_setpoint=1.02)

    print("Before injection:")
    print(f"Bus P_spec: {test_bus.P_spec}, Voltage (vpu): {test_bus.vpu}")

    # Inject power to the bus
    solar_unit.inject_power()

    print("\nAfter injection:")
    print(f"Bus P_spec: {test_bus.P_spec}, Voltage (vpu): {test_bus.vpu}")
    print(f"Solar Unit Per-Unit Output: {solar_unit.get_pu_generation()} pu")




#other code

class SolarPV:
    """
    The SolarPV class models a grid-connected solar PV generator.
    It injects real power (P) and maintains constant voltage magnitude like a PV bus.
    """

    def __init__(self, name: str, bus, rated_power: float, voltage_setpoint: float = 1.0):
        """
        Initialize the SolarPV generator.

        :param name: Name of the solar PV unit
        :param bus: Associated bus object
        :param rated_power: Rated power output in MW
        :param voltage_setpoint: Voltage setpoint in per unit (default 1.0)
        """
        self.name = name
        self.bus = bus
        self.rated_power = rated_power
        self.voltage_setpoint = voltage_setpoint

        self.validate()

    def validate(self):
        """
        Validates the rated power and voltage setpoint of the PV unit.
        """
        if self.rated_power < 0:
            raise ValueError(f"Rated power for {self.name} must be non-negative.")
        if not (0.9 <= self.voltage_setpoint <= 1.1):
            raise ValueError(f"Voltage setpoint for {self.name} must be within [0.9, 1.1] p.u.")

    def inject_power(self):
        """
        Apply power injection to the bus. Acts as a PV generator.
        """
        self.bus.P_spec += self.rated_power / 100  # convert to per unit on 100 MVA base
        self.bus.vpu = self.voltage_setpoint


# ☀️ Run validations if executed directly
if __name__ == '__main__':
    class DummyBus:
        def __init__(self, name):
            self.name = name
            self.P_spec = 0
            self.vpu = 1.0

    print("Running SolarPV validation tests...\n")

    # ✅ Valid PV
    try:
        bus = DummyBus("Bus A")
        pv = SolarPV("PV1", bus, rated_power=50, voltage_setpoint=1.0)
        pv.inject_power()
        print(f"{pv.name} successfully injected {pv.rated_power} MW at {pv.voltage_setpoint} p.u. to {pv.bus.name}")
    except ValueError as e:
        print("Failed valid PV test:", e)

    # ❌ Invalid power
    try:
        bus = DummyBus("Bus B")
        pv = SolarPV("PV2", bus, rated_power=-20, voltage_setpoint=1.0)
    except ValueError as e:
        print("Correctly caught invalid power:", e)

    # ❌ Invalid voltage
    try:
        bus = DummyBus("Bus C")
        pv = SolarPV("PV3", bus, rated_power=30, voltage_setpoint=1.2)
    except ValueError as e:
        print("Correctly caught invalid voltage:", e)
