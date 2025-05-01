# --- UPDATED solution.py with Solar PV Support ☀️ ---
import numpy as np

class Solution:
    def __init__(self, buses, ybus, voltages):
        """
        Initializes the Solution object with system data structures.
        :param buses: list of bus objects
        :param ybus: admittance matrix (numpy array)
        :param voltages: initial voltage magnitudes for each bus
        """
        self.buses = buses
        self.ybus = ybus
        self.voltages = voltages

    def initialize_system(self, circuit):
        """
        Initializes voltage and power specifications from circuit topology.
        Applies load subtraction and generator/solar power injections.
        Computes the Ybus matrix for use in power flow analysis.
        """
        # Initialize voltage and angle
        for bus in circuit.buses.values():
            bus.vpu = 1.0
            bus.delta = 0.0

        # Subtract load power from each bus's specification
        for load in circuit.loads.values():
            load.bus.P_spec -= load.real_power / 100
            load.bus.Q_spec -= load.reactive_power / 100

        # Add generator real power to each bus
        for gen in circuit.generators.values():
            gen.bus.P_spec += gen.mw_setpoint / 100

        # ☀️ Add solar PV generation to the bus
        for pv in circuit.solar_pvs.values():
            pv.bus.P_spec += pv.get_pu_generation(circuit.S_base)

        # Generate power flow Ybus matrix
        circuit.calc_ybus_powerflow()
        self.buses = list(circuit.buses.values())
        self.ybus = circuit.ybus  # updated: directly access Ybus matrix
        self.voltages = [bus.vpu for bus in self.buses]

    def compute_power_injection(self, bus_k_index, angles):
        """
        Computes real and reactive power injected at bus k using voltage magnitudes and angles.
        :param bus_k_index: index of target bus
        :param angles: list of bus voltage angles in degrees
        :return: P_k, Q_k (power injected in per unit)
        """
        P_k, Q_k = 0, 0
        V_k = self.voltages[bus_k_index]
        delta_k = np.radians(angles[bus_k_index])

        # Loop over all other buses to compute power flow contributions
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
        Computes the mismatch (ΔP, ΔQ) for each bus except Slack.
        This is used in the Newton-Raphson solver.
        :return: mismatch vectors for real and reactive power
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
        Prints the mismatch in power at each bus.
        Useful for debugging and checking convergence.
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
    Converts 3-phase ABC voltages to sequence components (0, 1, 2).
    :return: v0, v1, v2 (zero, positive, negative sequence)
    """
    a = np.exp(1j * 2 * np.pi / 3)
    v0 = (va + vb + vc) / 3
    v1 = (va + a * vb + a**2 * vc) / 3
    v2 = (va + a**2 * vb + a * vc) / 3
    return v0, v1, v2

def seq_to_abc(v0, v1, v2):
    """
    Converts symmetrical components (0, 1, 2) to phase voltages (A, B, C).
    :return: va, vb, vc (phase quantities)
    """
    a = np.exp(1j * 2 * np.pi / 3)
    va = v0 + v1 + v2
    vb = v0 + a**2 * v1 + a * v2
    vc = v0 + a * v1 + a**2 * v2
    return va, vb, vc
