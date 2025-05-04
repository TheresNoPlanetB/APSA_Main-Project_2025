from bus import Bus

class Load:

    """
    The load  class models consumptions.
    It has attributes name, bus, real_power, reactive_power.
    """

    def __init__(self, name: str, bus: Bus, real_power: float, reactive_power: float):
        self.name = name
        self.bus = bus
        self.real_power = real_power
        self.reactive_power = reactive_power

if __name__ == '__main__':
        from bus import Bus

        # Store buses and loads in lists
        buses = [
            Bus("Bus 2", 230, "PQ Bus"),
            Bus("Bus 3", 230, "PQ Bus"),
            Bus("Bus 4", 230, "PQ Bus"),
            Bus("Bus 5", 230, "PQ Bus"),
            Bus("Bus 6", 230, "PQ Bus"),
        ]

        loads = [
            Load("Load 2", buses[0], 80, 0),
            Load("Load 3", buses[1], 110, 50),
            Load("Load 4", buses[2], 100, 70),
            Load("Load 5", buses[3], 100, 65),
            Load("Load 6", buses[4], 23, 0),
        ]

        # Loop through loads and print info
        for load in loads:
            bus = load.bus
            print(
                f"Name: {load.name}, Bus: {bus.name} @ {bus.base_kv}V, "
                f"Real PWR: {load.real_power}W, Reactive PWR: {load.reactive_power}VAR")