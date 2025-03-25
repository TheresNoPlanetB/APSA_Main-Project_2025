import numpy as np
from solution import Solution

class Bus:
    """
    The Bus class models a bus in a power system.
    Each bus has a name and a nominal voltage level.
    """
    bus_count = 0
    # Class variable to keep count of bus instances

    def __init__(self, name, base_kv, bus_type, vpu = 1.0, delta = 0.0, P_spec = 0, Q_spec = 0):
        """
        Initialize the Bus object with the given parameters.
        """

        self.name = name  # Name of the bus
        self.base_kv = base_kv  # Nominal voltage level of the bus
        self.index = Bus.bus_count  # Unique index for the bus
        self.vpu = vpu # Given per unit voltage magnitude
        self.delta = delta # Given voltage phase angle in degrees
        self.bus_type = bus_type # Bus type (Slack, PQ, PV)
        self.P_spec = P_spec
        self.Q_spec = Q_spec
        self.validate_bus_type() # Validate bus type
        Bus.bus_count += 1 # Increment bus count

    def __str__(self):
        """
        Return a string representation of the Bus object.
        """
        return (f"Bus(name={self.name}, base_kv={self.base_kv}, bus_type={self.bus_type}, index={self.index}, "
                f"vpu={self.vpu},delta={self.delta})")

    """
    Validate bus_type by ensure bus_type is either PQ Bus, PV Bus or Slack Bus
    If not, null out bus, and report invalid bus type error
    """
    def validate_bus_type(self):
        if self.bus_type == "Slack Bus":
            self.bus_type = self.bus_type
        elif self.bus_type == "PV Bus":
            self.bus_type = self.bus_type
        elif self.bus_type == "PQ Bus":
            self.bus_type = self.bus_type
        else:
            self.name = "Invalid Bus Type Error"
            self.base_kv = "Invalid Bus Type Error"
            self.bus_type = "Invalid Bus Type Error"
            self.index = "Invalid Bus Type Error"
            print("Invalid Bus Type. Redefine Bus with bus type: PQ Bus, PV Bus or Slack Bus")

    def compute_power_mismatch(self, system_settings, voltages):
        """
        Compute power mismatch using SystemSettings for Newton-Raphson power flow.
        """
        mismatch_results = {}

        for bus in system_settings.buses:
            # Bus name is stored
            mismatch_results[bus.name] = {"Bus Name": bus.name}

            if bus.bus_type == "Slack Bus":
                mismatch_results[bus.name]["Delta P"] = None
                mismatch_results[bus.name]["Delta Q"] = None
                continue # Skip mismatch for slack bus

            # Compute actual power injection using SystemSettings function
            P_calc, Q_calc = system_settings.compute_power_injection(bus, voltages)

            # Calculate mismatch
            delta_P = round(bus.P_spec - P_calc, 2)
            delta_Q = round(bus.Q_spec - Q_calc, 2) if bus.bus_type == "PQ Bus" else None

            # Store mismatch in a dictionary using bus name
            mismatch_results[bus.name]["Delta P"] = delta_P
            mismatch_results[bus.name]["Delta Q"] = delta_Q

        return mismatch_results

if __name__ == '__main__':
    # Ybus matrix
    ybus = np.array([
        [1 + 2j, 3 + 4j, 5 + 6j],
        [7 + 8j, 9 + 10j, 11 + 12j],
        [13 + 14j, 15 + 16j, 17 + 18j]
    ])

    # Buses
    bus1 = Bus("Bus 1", 230, "Slack Bus")
    bus2 = Bus("Bus 2", 230, "PQ Bus", P_spec = 1.5, Q_spec = 0.5)
    bus3 = Bus("Bus 3", 230, "PV Bus", P_spec = 2.0)

    # System voltages (p.u.)
    voltages = np.array([
        1 + 0j,  # Slack Bus (1.0 p.u. with 0° angle)
        1.02 * np.exp(1j * np.radians(5)),  # PQ Bus (1.02 p.u., 5° angle)
        1.01 * np.exp(1j * np.radians(3))   # PV Bus (1.01 p.u., 3° angle)
    ])

    # Create SystemSettings instance
    system_settings = Solution(ybus, [bus1, bus2, bus3])

    # Compute mismatch
    mismatch_results = bus1.compute_power_mismatch(system_settings, voltages)

    # Print mismatch results per bus
    for bus_index, mismatches in mismatch_results.items():
        print(f"{bus_index}:")
        print(f" - Delta P: {mismatches.get('Delta P', 'N/A')}")
        print(f" - Delta Q: {mismatches.get('Delta Q', 'N/A')}")