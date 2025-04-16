from http.cookiejar import reach

from bus import Bus

class Generator:

    """
    The generator class models power injections.
    It has attributes name, bus, voltage_setpoint, mw_setpoint.
    """

    def __init__(self, name: str, bus: Bus, voltage_setpoint: float, mw_setpoint: float, reactance: float):
        self.name = name
        self.bus = bus
        self.voltage_setpoint = voltage_setpoint
        self.mw_setpoint = mw_setpoint
        self.reactance = reactance
        self.admittance = 1/self.reactance

if __name__ == '__main__':
    from bus import Bus

    buses = [
        Bus("Bus 7", 50, "PV Bus")
    ]

    generators = [
        Generator("Gen1", buses[0], 230, 145),
    ]

    for generator in generators:
        bus = generator.bus
        print(
            f"Name: {generator.name}, Bus: {bus.name}, Voltage: {bus.base_kv}V, " 
            f"Voltage Setpoint: {generator.voltage_setpoint}V, MW Setpoint: {generator.mw_setpoint}MW")