class Generator:

    """
    The generator class models power injections.
    It has attributes name, bus, voltage_setpoint, mw_setpoint.
    """

    def __init__(self, name, bus, voltage_setpoint, mw_setpoint):
        self.name = name
        self.bus = bus
        self.voltage_setpoint = voltage_setpoint
        self.mw_setpoint = mw_setpoint

if __name__ == '__main__':
    from generator import Generator
    from bus import Bus

    bus1 = Bus("bus1", 50, "PV Bus")
    generator1 = Generator("Gen1", bus1, 230, 145)
    print(f"Name: {generator1.name}, Bus: {bus1.name}, Voltage: {bus1.base_kv}V, Voltage Setpoint: {generator1.voltage_setpoint}V, MW Setpoint: {generator1.mw_setpoint}MW")

