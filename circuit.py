from bus import Bus
#from main import buses
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
        self.ybus_powerflow = None # Ybus matrix placeholder
        self.ybus_faultstudy = None # Ybus matrix placeholder
        self.zbus = None
        self.fault_current = None # Specific current at bus
        self.fault_currents = [] # List to store fault values
        self.fault_bus_v = None # Voltage at bus given fault on different bus
        self.fault_bus_vs = [] # List to store voltage values
        self.V_f = 1.0 # Pre-fault voltage in p.u.


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

    def add_generator(self, name, bus_name, voltage_setpoint, mw_setpoint, x1_pu, x2_pu, x0_pu, base_mva):
        if name in self.generators:
            raise ValueError(f"Generator {name} already exists in the circuit.")
        if bus_name not in self.buses:
            raise ValueError(f"Bus {bus_name} must be added before attaching a generator.")
        self.generators[name] = Generator(
            name, self.buses[bus_name], voltage_setpoint, mw_setpoint,
            x1_pu, x2_pu, x0_pu, base_mva
        )

    def add_load(self, name, bus_name, real_power, reactive_power):
        if name in self.loads:
            raise ValueError(f"Load {name} already exists in the circuit.")
        if bus_name not in self.buses:
            raise ValueError(f"Bus {bus_name} must be added before attaching a load.")
        self.loads[name] = Load(name, self.buses[bus_name], real_power, reactive_power)

    def calc_ybus_powerflow(self):
        # Ybus matrix by summing the primitive admittance matrices.

        # Initialize Ybus matrix (N x N zero matrix)
        N = len(self.buses)
        if N == 0:
            raise ValueError("No buses in the circuit to compute Ybus.")

        self.ybus_powerflow = np.zeros((N, N), dtype=complex)  # Initialize as complex numbers

        # Bus names to indices for Ybus
        bus_indices = {bus_name: idx for idx, bus_name in enumerate(self.buses.keys())}

        # Retrieve info from transformer
        for transformer in self.transformer.values():
            bus1, bus2 = transformer.bus1.name, transformer.bus2.name
            idx1, idx2 = bus_indices[bus1], bus_indices[bus2]
            Yprim = transformer.yprim  # Get primitive admittance matrix

            # Add self-admittance (diagonal elements)
            self.ybus_powerflow[idx1, idx1] += Yprim[0, 0]
            self.ybus_powerflow[idx2, idx2] += Yprim[1, 1]

            # Add mutual admittance (off-diagonal elements, negative values)
            self.ybus_powerflow[idx1, idx2] += Yprim[0, 1]
            self.ybus_powerflow[idx2, idx1] += Yprim[1, 0]
        # Retrieve info from transmission line
        for tline in self.transmission_lines.values():
            bus1, bus2 = tline.bus1.name, tline.bus2.name
            idx1, idx2 = bus_indices[bus1], bus_indices[bus2]
            Yprim = tline.yprim_pu  # Get primitive admittance matrix

            # Add self-admittance (diagonal elements)
            self.ybus_powerflow[idx1, idx1] += Yprim[0, 0]
            self.ybus_powerflow[idx2, idx2] += Yprim[1, 1]

            # Add mutual admittance (off-diagonal elements, negative values)
            self.ybus_powerflow[idx1, idx2] += Yprim[0, 1]
            self.ybus_powerflow[idx2, idx1] += Yprim[1, 0]

        # Numerical stability
        if np.any(np.diag(self.ybus_powerflow) == 0):
            raise ValueError("Singular Ybus detected. Ensure all buses have self-admittance.")

        # Add generator subtransient admittance (for power flow study)
        for generator in self.generators.values():
            bus_name = generator.bus.name
            idx = bus_indices[bus_name]
            if generator.x1_pu > 0:
                y_gen = 1 / (1j * generator.x1_pu)  # Subtransient admittance
                self.ybus_powerflow[idx, idx] += y_gen

    def calc_ybus_faultstudy(self, sequence: str = 'positive'):
        # Ybus matrix by summing the primitive admittance matrices.

        # Initialize Ybus matrix (N x N zero matrix)
        N = len(self.buses)
        if N == 0:
            raise ValueError("No buses in the circuit to compute Ybus.")

        self.ybus_faultstudy = np.zeros((N, N), dtype=complex)  # Initialize as complex numbers

        # Bus names to indices for Ybus
        bus_indices = {bus_name: idx for idx, bus_name in enumerate(self.buses.keys())}

        # Retrieve info from transformer and transmission line
        for transformer in self.transformer.values():
            bus1, bus2 = transformer.bus1.name, transformer.bus2.name
            idx1, idx2 = bus_indices[bus1], bus_indices[bus2]
            Yprim = transformer.yprim  # Get primitive admittance matrix

            # Add self-admittance (diagonal elements)
            self.ybus_faultstudy[idx1, idx1] += Yprim[0, 0]
            self.ybus_faultstudy[idx2, idx2] += Yprim[1, 1]

            # Add mutual admittance (off-diagonal elements, negative values)
            self.ybus_faultstudy[idx1, idx2] += Yprim[0, 1]
            self.ybus_faultstudy[idx2, idx1] += Yprim[1, 0]

        for tline in self.transmission_lines.values():
            bus1, bus2 = tline.bus1.name, tline.bus2.name
            idx1, idx2 = bus_indices[bus1], bus_indices[bus2]
            Yprim = tline.yprim_pu  # Get primitive admittance matrix

            # Add self-admittance (diagonal elements)
            self.ybus_faultstudy[idx1, idx1] += Yprim[0, 0]
            self.ybus_faultstudy[idx2, idx2] += Yprim[1, 1]

            # Add mutual admittance (off-diagonal elements, negative values)
            self.ybus_faultstudy[idx1, idx2] += Yprim[0, 1]
            self.ybus_faultstudy[idx2, idx1] += Yprim[1, 0]

        for generator in self.generators.values():
            bus_name = generator.bus.name
            idx = bus_indices[bus_name]

            if sequence == 'positive':
                x = generator.x1_pu
            elif sequence == 'negative':
                x = generator.x2_pu
            elif sequence == 'zero':
                x = generator.x0_pu
            else:
                continue

            if x > 0:
                y_gen = 1 / (1j * x)
                self.ybus_faultstudy[idx, idx] += y_gen

            # Numerical stability
        if np.any(np.diag(self.ybus_faultstudy) == 0):
            raise ValueError("Singular Ybus detected. Ensure all buses have self-admittance.")

    def calc_zbus(self):
        #calculate z bus
        self.zbus = np.linalg.inv(self.ybus_faultstudy)

    def calc_fault_current(self, Zbus, faulted_bus_num: int):
        """
        Calculate fault current at the faulted bus using provided Zbus matrix.
        Args:
            Zbus (np.ndarray): The Zbus matrix to use (typically with generator subtransients).
            faulted_bus_num (int): 1-based index of faulted bus
        """
        idx = faulted_bus_num - 1  # Convert to 0-based index
        self.fault_current = self.V_f / Zbus[idx, idx]
        self.fault_currents.append(self.fault_current)

    def print_fault_current(self, faulted_bus_num: int):
        print(f"Fault Current at Bus {faulted_bus_num} is {self.fault_current:.4f} pu")

    def calc_fault_bus_voltage(self, Zbus, faulted_bus_num: int, observed_bus_num: int):
        """
        Calculate voltage at an observed bus due to a fault at another bus.
        Args:
            Zbus (np.ndarray): The Zbus matrix used in fault calculation.
            faulted_bus_num (int): 1-based index of faulted bus
            observed_bus_num (int): 1-based index of observed bus
        """
        idx_fault = faulted_bus_num - 1
        idx_obs = observed_bus_num - 1
        self.fault_bus_v = (1.0 - Zbus[idx_fault, idx_obs] / Zbus[idx_fault, idx_fault]) * self.V_f
        self.fault_bus_vs.append(self.fault_bus_v)

    def print_fault_bus_voltage(self, observed_bus_num: int):
        print(f"Voltage at Bus {observed_bus_num} during fault is {self.fault_bus_v:.4f} pu")

    def get_zbus_with_generators(self):
        if self.zbus is None:
            raise ValueError("Zbus not yet calculated. Run calc_zbus() first.")
        return self.zbus

    def run_symmetrical_fault(self, faulted_bus_num: int):
        """
        Perform symmetrical fault analysis at a specific bus.
        Args:
            faulted_bus_num (int): 1-based index of the faulted bus
        """
        Zbus = self.get_zbus_with_generators()
        idx = faulted_bus_num - 1

        Zkk = Zbus[idx, idx]
        I_fault = self.V_f / Zkk
        self.fault_current = I_fault
        self.fault_currents.append(I_fault)

        # Header
        print(f"\n--- Symmetrical Fault at Bus {faulted_bus_num} ---")
        print(f"Zkk = {Zkk.real:.4f}{Zkk.imag:+.4f}j")
        print(f"I_fault = {I_fault.real:.4f}{I_fault.imag:+.4f}j pu, |I_fault| = {abs(I_fault):.4f} pu\n")

        # Calculate fault voltages at all buses
        self.fault_bus_vs = []
        print("Bus Voltages During Fault:")
        for bus_num in range(1, len(self.buses) + 1):
            idx_k = faulted_bus_num - 1
            idx_i = bus_num - 1
            V = (1.0 - Zbus[idx_k, idx_i] / Zbus[idx_k, idx_k]) * self.V_f
            self.fault_bus_vs.append(V)
            print(f"Bus {bus_num}: V = {V.real:.4f}{V.imag:+.4f}j pu")

    def get_ybus_powerflow(self):
        #Returns the computed Ybus matrix.
        if self.ybus_powerflow is None:
            raise ValueError("Ybus has not been computed. Run calc_ybus() first.")
        return self.ybus_powerflow

    def get_ybus_faultstudy(self):
        # Returns the computed Ybus matrix.
        if self.ybus_faultstudy is None:
            raise ValueError("Ybus has not been computed. Run calc_ybus() first.")
        return self.ybus_faultstudy

    # Print 7 Bus Power System Ybus Matrix
    def print_ybus_powerflow_table(self):
        # Format matrix elements as "real + imag j"
        formatted_matrix = [
            [f"Bus {i + 1}"] + [f"{elem.real:.2f}{elem.imag:+.2f}j" for elem in row]
            for i, row in enumerate(self.ybus_powerflow)
        ]

        # Print 7 Bus Power System Ybus Matrix
        print("\nYbus Admittance Matrix:")
        headers = ["Bus"] + [f"Bus {i + 1}" for i in range(len(self.ybus_powerflow))]
        print(tabulate(formatted_matrix, headers=headers, tablefmt="grid"))

    def print_ybus_faultstudy_table(self):
        # Format matrix elements as "real + imag j"
        formatted_matrix = [
            [f"Bus {i + 1}"] + [f"{elem.real:.2f}{elem.imag:+.2f}j" for elem in row]
            for i, row in enumerate(self.ybus_faultstudy)
        ]

        # Print 7 Bus Power System Ybus Matrix
        print("\nYbus with Generator Subtransient Reactance Included:")
        headers = ["Bus"] + [f"Bus {i + 1}" for i in range(len(self.ybus_faultstudy))]
        print(tabulate(formatted_matrix, headers=headers, tablefmt="grid"))

    def print_zbus_table(self):
        # Format matrix elements as "real + imag j"
        formatted_matrix = [
            [f"Bus {i + 1}"] + [f"{elem.real:.4f}{elem.imag:+.4f}j" for elem in row]
            for i, row in enumerate(self.zbus)
        ]

        # Print 7 Bus Power System Ybus Matrix
        print("\nZbus Matrix with Generator Subtransients:")
        headers = ["Bus"] + [f"Bus {i + 1}" for i in range(len(self.zbus))]
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