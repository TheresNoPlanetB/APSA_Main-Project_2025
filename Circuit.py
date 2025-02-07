from Bus import Bus
from Transformer import Transformer
from TransmissionLine import TransmissionLine
from Conductor import Conductor

class Circuit:
    def __init__(self,name):
        # Initializing attributes thru dictionaries
        self.name = name
        self.buses = {}
        self.transformer = {}
        self.transmission_line = {}

    def add_bus(self, name, base_kv):
        # Adding bus into circuit
        if name in self.buses:
            raise ValueError(f"Bus {name} already exists in the circuit.")
        self.buses[name] = Bus(name,base_kv)

    def add_transformer(self, name, bus1, bus2, power_rating, impedance_percent, x_over_r_ratio):
        # Adding transformer into circuit
        if name in self.transformer:
            raise ValueError(f"Transformer {name} already exists in the circuit.")
        if bus1 not in self.buses or bus2 not in self.buses:
            raise ValueError("Both buses must be added to the circuit before adding a transformer.")
        self.transformer[name] = Transformer(name, self.buses[bus1], self.buses[bus2], power_rating, impedance_percent, x_over_r_ratio)

    def add_transmission_line(self, name, bus1, bus2, bundle, geometry, length):
        # Adding transmission line into circuit
        if name in self.transmission_line:
            raise ValueError(f"Transmission line {name} already exists in the circuit.")
        if bus1 not in self.buses or bus2 not in self.buses:
            raise ValueError("Both buses must be added to the circuit before adding a transmission line.")
        self.transmission_line[name] = TransmissionLine(name, self.buses[bus1], self.buses[bus2], geometry, length)

    def __repr__(self):
        return (f"Circuit(name={self.name}, Buses={list(self.buses.keys())}, "
            f"Transformers={list(self.transformers.keys())}, "
            f"Transmission Lines={list(self.transmission_line.keys())})")
