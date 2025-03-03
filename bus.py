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
        self.vpu = 1
        self.delta = 0
        self.bus_type = "pq"
        self.validate_bus_type()
        Bus.bus_count += 1

    def __str__(self):
        """
        Return a string representation of the Bus object.
        """
        return f"Bus(name={self.name}, base_kv={self.base_kv}, bus_type={self.bus_type}, index={self.index})"

    """
    Define Bus_count and increment as per buses added
    """
    def set_bus_count(self, next_bus_count):
        self.index = next_bus_count

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



if __name__ == '__main__':
    from bus import Bus

    bus1 = Bus("Bus 1", 20, "Slack Bus")
    bus2 = Bus("Bus 2", 230, "PQ Bus")
    print("bus name: " + bus1.name, ", base kv: " + str(bus1.base_kv) + "kV", ", bus_type: " + bus1.bus_type, ", bus_ index: " + str(bus1.index))
    print("bus name: " + bus2.name, ", base kv: " + str(bus2.base_kv) + "kV", ", bus_type: " + bus2.bus_type, ", bus_ index: " + str(bus2.index))
    print(f"Total Number of Buses: {Bus.bus_count}")

