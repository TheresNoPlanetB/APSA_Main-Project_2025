from bus import Bus
from transformer import Transformer
from transmissionline import TransmissionLine
from generator import Generator
from load import Load
from solarpv import SolarPV  # ☀️ Added to support solar PV modeling
import numpy as np
from tabulate import tabulate
from sym_components import seq_to_abc


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
        self.solar_pvs = {}  # ☀️ Dictionary of SolarPV objects
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

    def add_transformer(self, name, bus1, bus2, power_rating, impedance_percent, x_over_r_ratio, base_mva, connection_type, zg1, zg2):
        # Adding transformer into circuit
        if name in self.transformer:
            raise ValueError(f"Transformer {name} already exists in the circuit.")
        if bus1 not in self.buses or bus2 not in self.buses:
            raise ValueError("Both buses must be added to the circuit before adding a transformer.")
        self.transformer[name] = Transformer(name, self.buses[bus1], self.buses[bus2], power_rating, impedance_percent, x_over_r_ratio, base_mva, connection_type, zg1, zg2)

    def add_transmission_line(self, name, bus1, bus2, bundle, geometry, length, connection_type):
        # Adding transmission line into circuit
        if name in self.transmission_lines:
            raise ValueError(f"Transmission line {name} already exists in the circuit.")
        if bus1 not in self.buses or bus2 not in self.buses:
            raise ValueError("Both buses must be added to the circuit before adding a transmission line.")
        self.transmission_lines[name] = TransmissionLine(name, self.buses[bus1], self.buses[bus2], bundle, geometry, length, connection_type)

    def add_generator(self, name, bus_name, voltage_setpoint, mw_setpoint, x1_pu, x2_pu, x0_pu, base_mva, grounded):
        if name in self.generators:
            raise ValueError(f"Generator {name} already exists in the circuit.")
        if bus_name not in self.buses:
            raise ValueError(f"Bus {bus_name} must be added before attaching a generator.")
        self.generators[name] = Generator(
            name, self.buses[bus_name], voltage_setpoint, mw_setpoint,
            x1_pu, x2_pu, x0_pu, base_mva, grounded
        )

    def add_solar_pv(self, name, bus_name, capacity_mw):
        # ☀️ Add solar PV to a bus in the system
        if name in self.solar_pvs:
            raise ValueError(f"SolarPV {name} already exists in the circuit.")
        if bus_name not in self.buses:
            raise ValueError(f"Bus {bus_name} must be added before attaching a SolarPV unit.")
        self.solar_pvs[name] = SolarPV(name, self.buses[bus_name], capacity_mw)

    def add_load(self, name, bus_name, real_power, reactive_power):
        if name in self.loads:
            raise ValueError(f"Load {name} already exists in the circuit.")
        if bus_name not in self.buses:
            raise ValueError(f"Bus {bus_name} must be added before attaching a load.")
        self.loads[name] = Load(name, self.buses[bus_name], real_power, reactive_power)

    # (no change to rest of code; leave all other functions intact)

    def network_summary(self):

        # Summarize buses
        bus_summary = "Buses in the Circuit:\n"
        for bus in self.buses.values():
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
                                    f"    Positive Sequence Yprim [pu]:\n{np.array2string(transformer.get_yprim('positive'), precision=4, separator=', ')}\n"
                                    f"    Negative Sequence Yprim [pu]:\n{np.array2string(transformer.get_yprim('negative'), precision=4, separator=', ')}\n"
                                    f"    Zero Sequence Yprim [pu]:\n{np.array2string(transformer.get_yprim('zero'), precision=4, separator=', ')}\n\n")

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

        solar_summary = "☀️ Solar PV Generators in the Circuit:\n"
        for pv in self.solar_pvs.values():
            solar_summary += (f"- {pv.name} on {pv.bus.name}: "
                              f"{pv.capacity_mw} MW (PV Bus)\n")

        network_summary = f"Network Summary for {self.name}:\n"
        network_summary += bus_summary + transformer_summary + transmission_line_summary + generator_summary + load_summary + solar_summary

        return network_summary