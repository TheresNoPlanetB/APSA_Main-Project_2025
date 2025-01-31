class Bus:
    """
    The Bus class models a bus in a power system.
    Each bus has a name and a nominal voltage level.
    """

    # Class variable to keep count of bus instances
    bus_count = 0

    def __init__(self, name, base_kv):
        """
        Initialize the Bus object with the given parameters.

        :param name: Name of the bus
        :param base_kv: Nominal voltage level of the bus (in kV)
        """
        self.name = name  # Name of the bus
        self.base_kv = base_kv  # Nominal voltage level of the bus
        self.index = Bus.bus_count  # Unique index for the bus

        # Increment the bus count for each new instance
        Bus.bus_count += 1

    def __str__(self):
        """
        Return a string representation of the Bus object.
        """
        return f"Bus(name={self.name}, base_kv={self.base_kv}, index={self.index})"

# Example usage:
# bus1 = Bus("Bus 1", 20)
# bus2 = Bus("Bus 2", 230)
#print(bus1)
#print(bus2)