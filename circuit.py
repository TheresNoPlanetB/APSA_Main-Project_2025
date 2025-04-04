from bus import Bus
from transformer import Transformer
from transmissionline import TransmissionLine
from generator import Generator
from load import Load
import numpy as np
from tabulate import tabulate


# Circuits are Cool :)

class Circuit:
    def __init__(self,name: str):
        # Initializing attributes thruough dictionaries
        self.name = name
        self.buses = {} # Dictionary of Bus objects
        self.transformer = {} # Dictionary of Transformer objects
        self.transmission_lines = {} # Dictionary of T-Line objects
        self.generators = {} # Dictionary of generators
        self.loads = {} # Dictionary of loads
        self.ybus = None # Ybus matrix placeholder

    def add_bus(self, name, base_kv, bus_type):
        # Adding bus into circuit
        if name in self.buses:
            raise ValueError(f"Bus {name} already exists in the circuit.")
        self.buses[name] = Bus(name, float(base_kv), str(bus_type))

    def add_transformer(self, name, bus1, bus2, power_rating, impedance_percent, x_over_r_ratio, base_mva):
        # Adding transformer into circuit
        if name in self.transformer:
            raise ValueError(f"Transformer {name} already exists in the circuit.")
        if bus1 not in self.buses or bus2 not in self.buses:
            raise ValueError("Both buses must be added to the circuit before adding a transformer.")
        self.transformer[name] = Transformer(name, self.buses[bus1], self.buses[bus2], power_rating, impedance_percent, x_over_r_ratio, base_mva)

    def add_transmission_line(self, name, bus1, bus2, bundle, geometry, length):
        # Adding transmission line into circuit
        if name in self.transmission_lines:
            raise ValueError(f"Transmission line {name} already exists in the circuit.")
        if bus1 not in self.buses or bus2 not in self.buses:
            raise ValueError("Both buses must be added to the circuit before adding a transmission line.")
        self.transmission_lines[name] = TransmissionLine(name, self.buses[bus1], self.buses[bus2], bundle, geometry, length)

    def add_generator(self, name, bus_name, voltage_setpoint, mw_setpoint):
        if name in self.generators:
            raise ValueError(f"Generator {name} already exists in the circuit.")
        if bus_name not in self.buses:
            raise ValueError(f"Bus {bus_name} must be added before attaching a generator.")
        self.generators[name] = Generator(name, self.buses[bus_name], voltage_setpoint, mw_setpoint)

    def add_load(self, name, bus_name, real_power, reactive_power):
        if name in self.loads:
            raise ValueError(f"Load {name} already exists in the circuit.")
        if bus_name not in self.buses:
            raise ValueError(f"Bus {bus_name} must be added before attaching a load.")
        self.loads[name] = Load(name, self.buses[bus_name], real_power, reactive_power)

    def calc_ybus(self):
        # Ybus matrix by summing the primitive admittance matrices.

        # Initialize Ybus matrix (N x N zero matrix)
        N = len(self.buses)
        if N == 0:
            raise ValueError("No buses in the circuit to compute Ybus.")

        self.ybus = np.zeros((N, N), dtype=complex)  # Initialize as complex numbers

        # Bus names to indices for Ybus
        bus_indices = {bus_name: idx for idx, bus_name in enumerate(self.buses.keys())}

        # Retrieve info from transformer and transmission line
        for transformer in self.transformer.values():
            bus1, bus2 = transformer.bus1.name, transformer.bus2.name
            idx1, idx2 = bus_indices[bus1], bus_indices[bus2]
            Yprim = transformer.yprim  # Get primitive admittance matrix

            # Add self-admittance (diagonal elements)
            self.ybus[idx1, idx1] += Yprim[0, 0]
            self.ybus[idx2, idx2] += Yprim[1, 1]

            # Add mutual admittance (off-diagonal elements, negative values)
            self.ybus[idx1, idx2] += Yprim[0, 1]
            self.ybus[idx2, idx1] += Yprim[1, 0]

        for tline in self.transmission_lines.values():
            bus1, bus2 = tline.bus1.name, tline.bus2.name
            idx1, idx2 = bus_indices[bus1], bus_indices[bus2]
            Yprim = tline.yprim_pu  # Get primitive admittance matrix

            # Add self-admittance (diagonal elements)
            self.ybus[idx1, idx1] += Yprim[0, 0]
            self.ybus[idx2, idx2] += Yprim[1, 1]

            # Add mutual admittance (off-diagonal elements, negative values)
            self.ybus[idx1, idx2] += Yprim[0, 1]
            self.ybus[idx2, idx1] += Yprim[1, 0]

        # Numerical stability
        if np.any(np.diag(self.ybus) == 0):
            raise ValueError("Singular Ybus detected. Ensure all buses have self-admittance.")

    def get_ybus(self):
        #Returns the computed Ybus matrix.
        if self.ybus is None:
            raise ValueError("Ybus has not been computed. Run calc_ybus() first.")
        return self.ybus

    # Print 7 Bus Power System Ybus Matrix
    def print_ybus_table(self):
        # Format matrix elements as "real + imag j"
        formatted_matrix = [
            [f"Bus {i + 1}"] + [f"{elem.real:.2f}{elem.imag:+.2f}j" for elem in row]
            for i, row in enumerate(self.ybus)
        ]

        # Print 7 Bus Power System Ybus Matrix
        print("\nYbus Admittance Matrix:")
        headers = ["Bus"] + [f"Bus {i + 1}" for i in range(len(self.ybus))]
        print(tabulate(formatted_matrix, headers=headers, tablefmt="grid"))

    # Print out summary of network
    def network_summary(self):

        # Summarize buses
        bus_summary = "Buses in the Circuit:\n"
        for bus in self.buses.values():  # Correctly accessing the values (which are dicts)
            bus_summary += f"- {bus.name} (Base kV: {bus.base_kv}, Bus Type: {bus.bus_type})\n"

        # Summarize transformers with more detailed information
        transformer_summary = "Transformers in the Circuit:\n"
        for transformer in self.transformer.values():
            transformer_summary += (f"- {transformer.name} (From {transformer.bus1.name} to {transformer.bus2.name})\n"
                                    f"    Power Rating: {transformer.power_rating} MVA\n"
                                    f"    Impedance: {transformer.impedance_percent}%\n"
                                    f"    X/R Ratio: {transformer.x_over_r_ratio}\n"
                                    f"    Base MVA: {transformer.base_mva} MVA\n"
                                    f"    Admittance Matrix (Yprim) [pu]: \n"
                                    f"{np.array2string(transformer.yprim, precision=4, separator=', ')}\n\n")

        # Summarize transmission lines with geometry info
        transmission_line_summary = "Transmission Lines in the Circuit:\n"
        for transmissionline in self.transmission_lines.values():
            transmission_line_geometry = transmissionline.geometry
            transmission_line_summary += (
                f"- {transmissionline.name} (From {transmissionline.bus1.name} to {transmissionline.bus2.name}, Length: {transmissionline.length} mi)\n"
                f"    Geometry: {transmission_line_geometry.name}, Deq: {transmission_line_geometry.Deq}\n"
                f"    Admittance Matrix (Yprim) [pu]: \n"
                f"{np.array2string(transmissionline.yprim_pu, precision=4, separator=', ')}\n\n")

        generator_summary = "Generators in the Circuit:\n"
        for generator in self.generators.values():
            generator_summary += (f"- {generator.name} on {generator.bus.name}: "
                                  f"{generator.voltage_setpoint} V setpoint, {generator.mw_setpoint} MW\n\n")

        load_summary = "Loads in the Circuit:\n"
        for load in self.loads.values():
            load_summary += (f"- {load.name} on {load.bus.name}: "
                             f"{load.real_power} W, {load.reactive_power} VAR \n\n")

        # Combine all summaries
        network_summary = f"Network Summary for {self.name}:\n"
        network_summary += bus_summary + transformer_summary + transmission_line_summary + generator_summary + load_summary

        return network_summary

    def __repr__(self):
        # Return a string representation of the circuit
        return (f"Circuit(name={self.name}, "
                f"Buses={list(self.buses.keys())}, "
                f"Transformers={list(self.transformer.keys())}, "
                f"Transmission Lines={list(self.transmission_lines.keys())})"
                f"Generators={list(self.generators.keys())})"
                f"Loads={list(self.loads.keys())})")

if __name__ == '__main__':
    from bus import Bus

    circuit1 = Circuit("Test Circuit")

    # Check attributes initialization
    print(circuit1.name)
    print(type(circuit1.name))
    print(circuit1.buses)
    print(type(circuit1.buses))

    # Add and retrieve equipment components
    circuit1.add_bus("Bus1", 230, "PQ Bus")
    print(circuit1.buses["Bus1"])
    print(type(circuit1.buses["Bus1"]))