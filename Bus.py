class Bus:
    """
    The Bus class models a bus in a power system.
    Each bus has a name and a nominal voltage level.
    """
    bus_count = 0
    # Class variable to keep count of bus instances

    def __init__(self, name, base_kv):
        """
        Initialize the Bus object with the given parameters.

        :param name: Name of the bus
        :param base_kv: Nominal voltage level of the bus (in kV)
        """

        self.name = name  # Name of the bus
        self.base_kv = base_kv  # Nominal voltage level of the bus
        self.index = Bus.bus_count  # Unique index for the bus
        Bus.bus_count += 1

    def __str__(self):
        """
        Return a string representation of the Bus object.
        """
        return f"Bus(name={self.name}, base_kv={self.base_kv}, index={self.index})"

    def set_bus_count(self, next_bus_count):
        self.index = next_bus_count



