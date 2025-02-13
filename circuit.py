from bus import Bus

from transformer import Transformer

from transmissionLine import TransmissionLine

class Circuit:
    def __init__(self,name,length):
        # Initializing attributes through the dictionaries

        self.name = name
        self.buses = {}
        self.transformer = {}
        self.transmission_line = {}
        self.length = length

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
        self.transmission_line[name] = (TransmissionLine(name, self.buses[bus1], self.buses[bus2], geometry, length))

    def __repr__(self):
        return (f"Circuit(name={self.name}, Buses={list(self.buses.keys())}, "
            f"Transformers={list(self.transformer.keys())}, "
            f"Transmission Lines={list(self.transmission_line.keys())})")

#Testing
"""
def main():
    # Create a Circuit instance
    circuit = Circuit("Test Circuit")

    # Add buses
    circuit.add_bus("Bus1", 20)
    circuit.add_bus("Bus2", 230)

    # Add a transformer
    circuit.add_transformer("T1", "Bus1", "Bus2", 125, 8.5, 10)

    # Add a transmission line
    conductor1 = Conductor("Partridge", 0.642, 0.0217, 0.385, 460)
    bundle1 = Bundle("Bundle 1", 2, 1.5, conductor1)
    geometry1 = Geometry("Geometry 1", 0, 0, 18.5, 0, 37, 0)
    circuit.add_transmission_line("Line1", "Bus1", "Bus2", bundle1, geometry1, 10)

    # Print the circuit details
    print(circuit)

if __name__ == "__main__":
    main()
"""