from bus import Bus
import numpy as np

class Generator:
    """
    The generator class models power injections.
    It includes base conversion to system base MVA.
    """
    def __init__(self, name: str, bus: Bus, voltage_setpoint: float, mw_setpoint: float,
                 x1_pu: float, x2_pu: float, x0_pu: float, base_mva: float, system_base_mva: float = 100.0):
        self.name = name
        self.bus = bus
        self.voltage_setpoint = voltage_setpoint
        self.mw_setpoint = mw_setpoint
        self.base_mva = base_mva
        self.system_base_mva = system_base_mva

        # Convert reactances to system base
        conversion_ratio = system_base_mva / base_mva
        self.x1_pu = x1_pu * conversion_ratio
        self.x2_pu = x2_pu * conversion_ratio
        self.x0_pu = x0_pu * conversion_ratio

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