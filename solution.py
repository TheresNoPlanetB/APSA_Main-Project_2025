# --- UPDATED solution.py with Solar PV Support ☀️ ---
import numpy as np

class Solution:
    def __init__(self, buses, ybus, voltages):
        """
        Initializes the Solution class with system data
        :param buses: list of bus objects
        :param ybus: system admittance matrix
        :param voltages: list of initial voltage magnitudes (pu)
        """
        self.buses = buses
        self.ybus = ybus
        self.voltages = voltages

    def initialize_system(self, circuit):
        """
        Initializes the bus voltage settings, sets loads and generator injections,
        and generates the Ybus matrix for power flow analysis.

        ☀️ Includes solar PV power injection at PV buses
        """
        for bus in circuit.buses.values():
            bus.vpu = 1.0
            bus.delta = 0.0

        for load in circuit.loads.values():
            load.bus.P_spec -= load.real_power / 100
            load.bus.Q_spec -= load.reactive_power / 100

        for gen in circuit.generators.values():
            gen.bus.P_spec += gen.mw_setpoint / 100

        # ☀️ Inject real power from solar PV units
        for pv in circuit.solar_pvs.values():
            pv.bus.P_spec += pv.get_pu_generation(circuit.S_base)

        circuit.calc_ybus_powerflow()
        self.buses = list(circuit.buses.values())
        self.ybus = circuit.get_ybus_powerflow()
        self.voltages = [bus.vpu for bus in self.buses]

    def compute_power_injection(self, bus_k_index, angles):
        """
        Calculates the real and reactive power injected at a given bus index.
        :param bus_k_index: index of the bus to calculate power injection for
        :param angles: list of voltage angles in degrees
        :return: P_k, Q_k real and reactive power at the bus (pu)
        """
        P_k, Q_k = 0, 0
        V_k = self.voltages[bus_k_index]
        delta_k = np.radians(angles[bus_k_index])

        for n in range(len(self.voltages)):
            V_n = self.voltages[n]
            delta_n = np.radians(angles[n])
            Y_kn = self.ybus[bus_k_index, n]
            Y_mag = np.abs(Y_kn)
            Y_angle = np.angle(Y_kn)
            angle_diff = delta_k - delta_n - Y_angle
            P_k += V_k * V_n * Y_mag * np.cos(angle_diff)
            Q_k += V_k * V_n * Y_mag * np.sin(angle_diff)

        return P_k, Q_k

    def compute_power_mismatch_vector(self):
        """
        Computes mismatch vector ΔP and ΔQ for non-slack buses.
        :return: numpy arrays delta_P, delta_Q
        """
        delta_P, delta_Q = [], []
        angles = [bus.delta for bus in self.buses]

        for bus in self.buses:
            if bus.bus_type == "Slack Bus":
                delta_P.append(0)
                delta_Q.append(0)
                continue

            P_calc, Q_calc = self.compute_power_injection(bus.index, angles)
            dP = bus.P_spec - P_calc
            dQ = bus.Q_spec - Q_calc if bus.bus_type == "PQ Bus" else 0
            delta_P.append(dP)
            delta_Q.append(dQ)

        return np.array(delta_P), np.array(delta_Q)

    def print_power_mismatch(self, delta_P, delta_Q):
        """
        Print power mismatches for each bus.
        """
        print("\n--- Power Mismatch ---")
        for i, bus in enumerate(self.buses):
            print(f"{bus.name} ({bus.bus_type}):")
            print(f"  MW:   {delta_P[i]: .5f}")
            print(f"  MVAR: {delta_Q[i]: .5f}")


# ---------------------------------------------------------------
# Symmetrical Component Transformation Utilities
# ---------------------------------------------------------------

def abc_to_seq(va, vb, vc):
    """
    Transform 3-phase quantities (abc) to symmetrical components (012)
    :param va: phase A quantity
    :param vb: phase B quantity
    :param vc: phase C quantity
    :return: v0, v1, v2 (zero, positive, negative sequence components)
    """
    a = np.exp(1j * 2 * np.pi / 3)
    v0 = (va + vb + vc) / 3
    v1 = (va + a * vb + a**2 * vc) / 3
    v2 = (va + a**2 * vb + a * vc) / 3
    return v0, v1, v2

def seq_to_abc(v0, v1, v2):
    """
    Transform symmetrical components (012) to 3-phase quantities (abc)
    :param v0: zero sequence component
    :param v1: positive sequence component
    :param v2: negative sequence component
    :return: va, vb, vc (phase quantities)
    """
    a = np.exp(1j * 2 * np.pi / 3)
    va = v0 + v1 + v2
    vb = v0 + a**2 * v1 + a * v2
    vc = v0 + a * v1 + a**2 * v2
    return va, vb, vc


# ---------------------------------------------------------------
# ☀️ Validation Example
# ---------------------------------------------------------------
if __name__ == '__main__':
    from circuit import Circuit
    from conductor import Conductor
    from bundle import Bundle
    from geometry import Geometry
    from solarpv import SolarPV

    # Create and define test circuit
    circuit1 = Circuit("Solar-Powered Circuit")

    # Add Buses
    circuit1.add_bus("Bus 1", 20, "Slack Bus")
    circuit1.add_bus("Bus 2", 230, "PQ Bus")
    circuit1.add_bus("Bus 3", 230, "PQ Bus")
    circuit1.add_bus("Bus 4", 230, "PQ Bus")
    circuit1.add_bus("Bus 5", 230, "PQ Bus")
    circuit1.add_bus("Bus 6", 230, "PQ Bus")
    circuit1.add_bus("Bus 7", 18, "PV Bus")

    # Add Transformers
    circuit1.add_transformer("T1", "Bus 1", "Bus 2", 125, 8.5, 10, 100, "Y-Y", 0, 0)
    circuit1.add_transformer("T2", "Bus 6", "Bus 7", 200, 10.5, 12, 100, "Y-Y", 0, 0)

    # Define transmission line parameters
    conductor1 = Conductor("Partridge", 0.642, 0.0217, 0.385, 460)
    bundle1 = Bundle("Bundle A", 2, 1.5, conductor1)
    geometry1 = Geometry("Geometry 1", 0, 0, 19.5, 0, 39, 0)

    # Add Transmission Lines
    circuit1.add_transmission_line("Line 1", "Bus 2", "Bus 4", bundle1, geometry1, 10, "Transposed")
    circuit1.add_transmission_line("Line 2", "Bus 2", "Bus 3", bundle1, geometry1, 25, "Transposed")
    circuit1.add_transmission_line("Line 3", "Bus 3", "Bus 5", bundle1, geometry1, 20, "Transposed")
    circuit1.add_transmission_line("Line 4", "Bus 4", "Bus 6", bundle1, geometry1, 20, "Transposed")
    circuit1.add_transmission_line("Line 5", "Bus 5", "Bus 6", bundle1, geometry1, 10, "Transposed")
    circuit1.add_transmission_line("Line 6", "Bus 4", "Bus 5", bundle1, geometry1, 35, "Transposed")

    # Add Loads
    circuit1.add_load("Load 3", "Bus 3", 110, 50)
    circuit1.add_load("Load 4", "Bus 4", 100, 70)
    circuit1.add_load("Load 5", "Bus 5", 100, 65)

    # Add Generators
    circuit1.add_generator("G1", "Bus 1", 1.0, 113.56, 0.1, 0.1, 0.05, 100, True)
    circuit1.add_generator("G2", "Bus 7", 1.0, 200, 0.1, 0.1, 0.05, 100, True)

    # ☀️ Add Solar PV
    circuit1.add_solar_pv("PV1", "Bus 5", rated_power=50, voltage_setpoint=1.0)

    # Run validation
    solution = Solution(buses=[], ybus=None, voltages=[])
    solution.initialize_system(circuit1)

    # Compute power mismatches
    delta_P, delta_Q = solution.compute_power_mismatch_vector()

    # Display mismatch results
    print("\n--- Power Mismatch ---")
    for i, bus in enumerate(solution.buses):
        print(f"{bus.name} ({bus.bus_type}):")
        print(f"  MW:   {delta_P[i]: .5f}")
        print(f"  MVAR: {delta_Q[i]: .5f}")
