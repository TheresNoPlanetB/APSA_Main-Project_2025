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