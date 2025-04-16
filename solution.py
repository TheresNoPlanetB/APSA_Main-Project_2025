import numpy as np

class Solution:
    def __init__(self, buses, ybus, voltages):
        """
        Initializes the system settings class with Ybus and buses.
        :param buses: list of bus object
        :param ybus: system admittance matrix
        :param voltages: voltage vector
        """
        self.buses = buses # System admittance matrix
        self.ybus = ybus # List of bus objects
        self.voltages = voltages # List of voltage magnitudes (per uint) for all buses

    def initialize_system(self, circuit):
        """
        Initializes bus voltages, loads, generators, and calculates Ybus.
        """
        # Set voltage and angle for all buses
        # Example hard-coded values

        # Set voltage and angle for all buses
        for bus in circuit.buses.values():
            bus.vpu = 1.0
            bus.delta = 0.0

        # Set load powers (as negative injections)
        for load in circuit.loads.values():
            load.bus.P_spec -= load.real_power / 100 # Converted from MW to p.u. by dividing by 100
            load.bus.Q_spec -= load.reactive_power / 100 # Converted from MVAR to p.u. by dividing by 100

        # Set generator real power contributions
        for gen in circuit.generators.values():
            gen.bus.P_spec += gen.mw_setpoint / 100 # Converted from MW to p.u. by dividing by 100

        # Calculate Ybus and update internal state
        circuit.calc_ybus_powerflow()
        self.buses = list(circuit.buses.values())
        self.ybus = circuit.get_ybus_powerflow()
        self.voltages = [bus.vpu for bus in self.buses]

    def compute_power_injection(self, bus_k_index, angles):
        """
        Calculate real and reactive power at specific bus.
        bus_k_index: index of the bus you're calculating power injection for (k)
        angles: list of voltage angles (in degrees) for all buses
        """
        P_k = 0  # Total real power injection at bus k
        Q_k = 0  # Total reactive power injection at bus k
        V_k = self.voltages[bus_k_index]  # Voltage magnitude at bus k
        delta_k = np.radians(angles[bus_k_index])  # Voltage angle at bus k (in radians)

        #print(f"\n--- Calculating Power Injection for Bus {bus_k_index + 1} ---")
        #print(f"V_k = {V_k:.2f}, δ_k (rad) = {delta_k:.2f}")

        for n in range(len(self.voltages)):
            V_n = self.voltages[n]
            delta_n = np.radians(angles[n])
            Y_kn = self.ybus[bus_k_index, n]
            Y_mag = np.abs(Y_kn)
            Y_angle = np.angle(Y_kn)

            angle_diff = delta_k - delta_n - Y_angle

            # Calculate each term in the power summation
            term_P = V_k * V_n * Y_mag * np.cos(angle_diff)
            term_Q = V_k * V_n * Y_mag * np.sin(angle_diff)

            # Accumulate total power injections
            P_k += term_P
            Q_k += term_Q

            # Print term details
            #print(f"\nTerm {n + 1}:")
            #print(f"  V_n = {V_n:.2f}, δ_n (rad) = {delta_n:.2f}")
            #print(f"  |Y_kn| = {Y_mag:.2f}, ∠Y_kn = {Y_angle:.2f} rad")
            #print(f"  θ_diff = {angle_diff:.2f}")
            #print(f"  P_term = {term_P:.2f}, Q_term = {term_Q:.2f}")

        #print(f"\nTotal P_inj = {P_k:.2f} p.u. ({P_k * 100:.2f} MW)")
        #print(f"Total Q_inj = {Q_k:.2f} p.u. ({Q_k * 100:.2f} MVAR)")

        return P_k, Q_k

    def compute_power_mismatch_vector(self):
        """
        Computes the full power mismatch vector ΔP and ΔQ for all non-slack buses.
        Returns a NumPy array representing the mismatch vector used in Newton-Raphson.
        """
        delta_P = []
        delta_Q = []
        angles = [bus.delta for bus in self.buses]  # degrees

        #print("\n--- Power Mismatch Calculations ---")

        for bus in self.buses:
            if bus.bus_type == "Slack Bus":
                delta_P.append(0)
                delta_Q.append(0)
                continue  # Skip slack bus

            # Compute injected power
            P_calc, Q_calc = self.compute_power_injection(bus.index, angles)

            # Compute mismatch (multiply by 100 to convert from p.u. to MW/MVAR)
            dP = (bus.P_spec - P_calc)
            dQ = (bus.Q_spec - Q_calc) if bus.bus_type == "PQ Bus" else 0

            # Append to vectors
            delta_P.append(dP)
            delta_Q.append(dQ)

            # Print detailed info
            #print(f"\nBus {bus.name} ({bus.bus_type}):")
            #print(f"  P_spec = {bus.P_spec * 100:.2f} MW,  P_calc = {P_calc * 100:.2f} MW → ΔP = {dP:.4f} MW")
            #print(f"  Q_spec = {bus.Q_spec * 100:.2f} MVAR, Q_calc = {Q_calc * 100:.2f} MVAR → ΔQ = {dQ:.4f} MVAR")

        return np.array(delta_P), np.array(delta_Q)

    def print_power_mismatch(self, delta_P, delta_Q):
        print("\n--- Power Mismatch ---")
        for i, bus in enumerate(self.buses):
            print(f"{bus.name} ({bus.bus_type}):")
            print(f"  MW:   {delta_P[i]: .5f}")
            print(f"  MVAR: {delta_Q[i]: .5f}")

if __name__ == "__main__":

    from circuit import Circuit
    from conductor import Conductor
    from bundle import Bundle
    from geometry import Geometry

    # Create circuit
    circuit1 = Circuit("Circuit")

    # Add Buses
    circuit1.add_bus("Bus 1", 20, "Slack Bus")
    circuit1.add_bus("Bus 2", 230, "PQ Bus")
    circuit1.add_bus("Bus 3", 230, "PQ Bus")
    circuit1.add_bus("Bus 4", 230, "PQ Bus")
    circuit1.add_bus("Bus 5", 230, "PQ Bus")
    circuit1.add_bus("Bus 6", 230, "PQ Bus")
    circuit1.add_bus("Bus 7", 18, "PV Bus")

    # Add Transformers
    circuit1.add_transformer("T1", "Bus 1", "Bus 2", 125, 8.5, 10, 100)
    circuit1.add_transformer("T2", "Bus 6", "Bus 7", 200, 10.5, 12, 100)

    # Add Transmission Line Parameters
    conductor1 = Conductor("Partridge", 0.642, 0.0217, 0.385, 460)
    bundle1 = Bundle("Bundle A", 2, 1.5, conductor1)
    geometry1 = Geometry("Geometry 1", 0, 0, 19.5, 0, 39, 0)

    # Add Transmission Lines
    circuit1.add_transmission_line("Line 1", "Bus 2", "Bus 4", bundle1, geometry1, 10)
    circuit1.add_transmission_line("Line 2", "Bus 2", "Bus 3", bundle1, geometry1, 25)
    circuit1.add_transmission_line("Line 3", "Bus 3", "Bus 5", bundle1, geometry1, 20)
    circuit1.add_transmission_line("Line 4", "Bus 4", "Bus 6", bundle1, geometry1, 20)
    circuit1.add_transmission_line("Line 5", "Bus 5", "Bus 6", bundle1, geometry1, 10)
    circuit1.add_transmission_line("Line 6", "Bus 4", "Bus 5", bundle1, geometry1, 35)

    # Add Load
    circuit1.add_load("Load 3", "Bus 3", 110, 50)
    circuit1.add_load("Load 4", "Bus 4", 100, 70)
    circuit1.add_load("Load 5", "Bus 5", 100, 65)

    # Add Generator
    circuit1.add_generator("G1", "Bus 1", 1.0, 113.56)
    circuit1.add_generator("G2", "Bus 7", 1.0, 200)
    ### Add rated voltage to generator class

    # Run validation
    solution = Solution(buses=[], ybus=None, voltages=[])
    solution.initialize_system(circuit1)

    # Power Mismatch
    delta_P, delta_Q = solution.compute_power_mismatch_vector()

    print("\n--- Power Mismatch ---")
    for i, bus in enumerate(solution.buses):
        print(f"{bus.name} ({bus.bus_type}):")
        print(f"  MW:   {delta_P[i]: .5f}")
        print(f"  MVAR: {delta_Q[i]: .5f}")