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
    def __init__(self, name: str):
        # Initializing attributes through dictionaries
        self.name = name
        self.buses = {}               # Dictionary of Bus objects
        self.transformer = {}         # Dictionary of Transformer objects
        self.transmission_lines = {}  # Dictionary of T-Line objects
        self.generators = {}          # Dictionary of generators
        self.loads = {}               # Dictionary of loads
        self.solar_pvs = {}           # ☀️ Dictionary of SolarPV objects
        self.S_base = 100.0  # System base MVA
        self.ybus_powerflow = None    # Ybus matrix for power flow studies
        self.ybus_faultstudy = None   # Ybus matrix for fault studies
        self.zbus = None              # Zbus matrix
        self.fault_current = None     # Symmetrical fault current at a bus
        self.V_f = 1.0                # Pre-fault voltage in p.u.

    def add_bus(self, name, base_kv, bus_type):
        if name in self.buses:
            raise ValueError(f"Bus {name} already exists in the circuit.")
        self.buses[name] = Bus(name, float(base_kv), str(bus_type))

    def add_transformer(self, name, bus1, bus2, power_rating, impedance_percent,
                        x_over_r_ratio, base_mva, connection_type, zg1, zg2):
        if name in self.transformer:
            raise ValueError(f"Transformer {name} already exists in the circuit.")
        if bus1 not in self.buses or bus2 not in self.buses:
            raise ValueError("Both buses must be added to the circuit before adding a transformer.")
        self.transformer[name] = Transformer(
            name,
            self.buses[bus1],
            self.buses[bus2],
            power_rating,
            impedance_percent,
            x_over_r_ratio,
            base_mva,
            connection_type,
            zg1,
            zg2
        )

    def add_transmission_line(self, name, bus1, bus2, bundle, geometry, length, connection_type):
        if name in self.transmission_lines:
            raise ValueError(f"Transmission line {name} already exists in the circuit.")
        if bus1 not in self.buses or bus2 not in self.buses:
            raise ValueError("Both buses must be added to the circuit before adding a transmission line.")
        self.transmission_lines[name] = TransmissionLine(
            name,
            self.buses[bus1],
            self.buses[bus2],
            bundle,
            geometry,
            length,
            connection_type
        )

    def add_generator(self, name, bus_name, voltage_setpoint, mw_setpoint,
                      x1_pu, x2_pu, x0_pu, base_mva, grounded):
        if name in self.generators:
            raise ValueError(f"Generator {name} already exists in the circuit.")
        if bus_name not in self.buses:
            raise ValueError(f"Bus {bus_name} must be added before attaching a generator.")
        self.generators[name] = Generator(
            name,
            self.buses[bus_name],
            voltage_setpoint,
            mw_setpoint,
            x1_pu,
            x2_pu,
            x0_pu,
            base_mva,
            grounded
        )

    def add_solar_pv(self, name, bus_name, capacity_mw):
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

    def network_summary(self):
        # Summarize buses
        bus_summary = "Buses in the Circuit:\n"
        for bus in self.buses.values():
            bus_summary += f"- {bus.name} (Base kV: {bus.base_kv}, Bus Type: {bus.bus_type})\n"

        # Transformer summary
        transformer_summary = "Transformers in the Circuit:\n"
        for transformer in self.transformer.values():
            transformer_summary += (
                f"- {transformer.name} (From {transformer.bus1.name} to {transformer.bus2.name})\n"
                f"    Power Rating: {transformer.power_rating} MVA\n"
                f"    Impedance: {transformer.impedance_percent}%\n"
                f"    X/R Ratio: {transformer.x_over_r_ratio}\n"
            )

        # Transmission line summary
        tx_summary = "Transmission Lines in the Circuit:\n"
        for tl in self.transmission_lines.values():
            tx_summary += (
                f"- {tl.name} (From {tl.bus1.name} to {tl.bus2.name}, Length: {tl.length} mi)\n"
            )

        # Generator summary
        gen_summary = "Generators in the Circuit:\n"
        for gen in self.generators.values():
            gen_summary += f"- {gen.name} on {gen.bus.name}: {gen.mw_setpoint} MW setpoint\n"

        # Load summary
        load_summary = "Loads in the Circuit:\n"
        for ld in self.loads.values():
            load_summary += f"- {ld.name} on {ld.bus.name}: {ld.real_power} W, {ld.reactive_power} VAR\n"

        # Solar PV summary
        pv_summary = "☀️ Solar PV in the Circuit:\n"
        for pv in self.solar_pvs.values():
            pv_summary += f"- {pv.name} on {pv.bus.name}: {pv.capacity_mw} MW\n"

        return (
            f"Network Summary for {self.name}:\n" +
            bus_summary + transformer_summary + tx_summary +
            gen_summary + load_summary + pv_summary
        )

    # Helper to map bus name to index
    def _bus_index(self, name):
        return list(self.buses.keys()).index(name)

    # Generic matrix printer
    def _print_matrix(self, mat, title="Matrix"):
        headers = list(self.buses.keys())
        rows = [[f"{val:.4f}" for val in row] for row in mat]
        print(f"\n{title}")
        print(tabulate(rows, headers=headers, showindex=headers, tablefmt="grid"))

    # Build Ybus for any sequence (positive, negative, zero)
    def calc_ybus(self, sequence='positive'):
        nb = len(self.buses)
        Y = np.zeros((nb, nb), dtype=complex)
        names = list(self.buses.keys())
        # Transformers
        for tr in self.transformer.values():
            yprim = tr.get_yprim(sequence)
            i = names.index(tr.bus1.name)
            j = names.index(tr.bus2.name)
            Y[i,i] += yprim[0,0]
            Y[j,j] += yprim[1,1]
            Y[i,j] += yprim[0,1]
            Y[j,i] += yprim[1,0]
        # Transmission lines
        for tl in self.transmission_lines.values():
            try:
                yprim = tl.get_yprim(sequence)
            except AttributeError:
                yprim = tl.yprim_pu  # assume positive-sequence only
            i = names.index(tl.bus1.name)
            j = names.index(tl.bus2.name)
            Y[i,i] += yprim[0,0]
            Y[j,j] += yprim[1,1]
            Y[i,j] += yprim[0,1]
            Y[j,i] += yprim[1,0]
        return Y

    # Compute Ybus for power flow
    def calc_ybus_powerflow(self):
        self.ybus_powerflow = self.calc_ybus('positive')
        return self.ybus_powerflow

    # Compute Ybus for fault study
    def calc_ybus_faultstudy(self, sequence='positive'):
        self.ybus_faultstudy = self.calc_ybus(sequence)
        return self.ybus_faultstudy

    # Compute Zbus (invert Ybus for fault study)
    def calc_zbus(self):
        if self.ybus_faultstudy is None:
            raise ValueError("Fault study Ybus not computed.")
        self.zbus = np.linalg.inv(self.ybus_faultstudy)
        return self.zbus

    def get_ybus_faultstudy(self):
        return self.ybus_faultstudy

    # Pretty-print Ybus for powerflow
    def print_ybus_powerflow_table(self):
        if self.ybus_powerflow is None:
            raise ValueError("Powerflow Ybus not computed.")
        self._print_matrix(self.ybus_powerflow, "Power Flow Ybus")

    # Pretty-print Ybus for fault study
    def print_ybus_faultstudy_table(self):
        if self.ybus_faultstudy is None:
            raise ValueError("Fault study Ybus not computed.")
        self._print_matrix(self.ybus_faultstudy, "Fault Study Ybus")

    # Pretty-print Zbus
    def print_zbus_table(self):
        if self.zbus is None:
            raise ValueError("Zbus not computed.")
        self._print_matrix(self.zbus, "Zbus Matrix")

    # Symmetrical 3-phase fault current
    def run_sym_fault(self, fault_bus_number):
        idx = list(self.buses.keys()).index(f"Bus {fault_bus_number}")
        Ifault = self.V_f / self.zbus[idx, idx]
        print(f"Symmetrical fault current at Bus {fault_bus_number}: {Ifault:.4f} pu")
        return Ifault

    # Placeholder for asymmetrical fault types
    def run_asym_fault(self, fault_type, fault_bus_number):
        raise NotImplementedError(f"Asymmetrical fault analysis ({fault_type}) not implemented.")