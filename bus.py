"""
bus.py
Defines the Bus class for modeling nodes (buses) in a power system network.
Each bus holds voltage magnitude, voltage angle, P/Q specifications, and type.
"""

class Bus:
    # Class variable to assign a unique index to each Bus instance
    bus_count = 0

    def __init__(self, name, base_kv, bus_type, vpu=1.0, delta=0.0, P_spec=0, Q_spec=0):
        """
        Initialize a Bus object.

        :param name:   Unique identifier for the bus (e.g., 'Bus 1').
        :param base_kv: Nominal voltage level of the bus in kilovolts (kV).
        :param bus_type: Type of bus; must be one of 'Slack Bus', 'PV Bus', or 'PQ Bus'.
        :param vpu:    Initial per-unit voltage magnitude (default 1.0 pu).
        :param delta:  Initial voltage phase angle in degrees (default 0.0°).
        :param P_spec: Specified real power injection in per-unit (positive for generation, negative for load).
        :param Q_spec: Specified reactive power injection in per-unit (positive for injection, negative for demand).
        """
        # Store input parameters as instance attributes
        self.name = name                # Bus label for identification in matrices and summaries
        self.base_kv = base_kv          # Nominal voltage level, used for per-unit conversions
        self.bus_type = bus_type        # Operational category (Slack, PV, or PQ)
        self.vpu = vpu                  # Current per-unit voltage magnitude
        self.delta = delta              # Current voltage phase angle in degrees
        self.P_spec = P_spec            # Real power setpoint (P) in pu
        self.Q_spec = Q_spec            # Reactive power setpoint (Q) in pu

        # Validate that bus_type is one of the accepted categories; raises ValueError if not
        self.validate_bus_type()

        # Assign a zero-based unique index used when building Ybus/Zbus matrices
        self.index = Bus.bus_count
        Bus.bus_count += 1

    def __str__(self):
        """
        Provide a human-readable representation, useful for debug prints.
        Example: Bus(name=Bus 1, base_kV=230.0, type=Slack Bus, index=0, vpu=1.0, delta=0.0)
        """
        return (
            f"Bus(name={self.name}, base_kV={self.base_kv}, type={self.bus_type}, "
            f"index={self.index}, vpu={self.vpu}, delta={self.delta})"
        )

    def validate_bus_type(self):
        """
        Ensure the bus_type attribute is valid and recognized by the simulator.

        Accepted types:
          - 'Slack Bus': Reference bus with fixed voltage magnitude and angle (balance of losses).
          - 'PV Bus':    Generator bus with fixed voltage magnitude and specified real power injection.
          - 'PQ Bus':    Load bus with specified real and reactive power demands.

        Raises:
          ValueError: If bus_type is not one of the accepted strings.
        """
        valid_types = ("Slack Bus", "PV Bus", "PQ Bus")
        if self.bus_type not in valid_types:
            # Unrecognized bus_type -> raise an exception and prevent creation
            raise ValueError(
                f"Invalid bus type '{self.bus_type}'. Must be one of {valid_types}."
            )

# Smoke-test when executed directly
if __name__ == '__main__':
    # Example of valid bus creation
    bus1 = Bus("Bus1", 230.0, "PQ Bus")
    print(bus1)

    # Example of invalid bus_type -> triggers ValueError
    try:
        Bus("X", 115.0, "InvalidType")
    except ValueError as err:
        print("Caught error as expected:", err)
