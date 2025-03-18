class Load:

    """
    The load  class models consumptions.
    It has attributes name, bus, real_power, reactive_power.
    """

    def __init__(self, name, bus, real_power, reactive_power):
        self.name = name
        self.bus = bus
        self.real_power = real_power
        self.reactive_power = reactive_power

if __name__ == '__main__':
    from load import Load
    from bus import Bus

    bus1 = Bus("bus1", 50, "PV Bus")
    load1 = Load("Load1", bus1, 230, 145)
    print(f"Name: {load1.name}, Bus: {bus1.name} @ {bus1.base_kv}V, real_power: {load1.real_power}W, reactive_power: {load1.reactive_power}VAR")

