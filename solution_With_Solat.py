import numpy as np

class SolutionSolarPV:
    def __init__(self, buses, ybus, voltages):
        self.buses = buses
        self.ybus = ybus
        self.voltages = voltages

    def initialize_system(self, circuit):
        for bus in circuit.buses.values():
            bus.vpu = 1.0
            bus.delta = 0.0

        for load in circuit.loads.values():
            load.bus.P_spec -= load.real_power / 100  # Convert kW to pu
            load.bus.Q_spec -= load.reactive_power / 100

        for gen in circuit.generators.values():
            gen.bus.P_spec += gen.mw_setpoint / 100

        # NOTE: Solar PV injections should already modify P_spec when added via add_solar_pv()

        circuit.calc_ybus_powerflow()
        self.buses = list(circuit.buses.values())
        self.ybus = circuit.get_ybus_powerflow()
        self.voltages = [bus.vpu for bus in self.buses]

    def compute_power_injection(self, bus_k_index, angles):
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
        delta_P, delta_Q = [], []
        angles = [bus.delta for bus in self.buses]

        for i, bus in enumerate(self.buses):
            if bus.bus_type == "Slack Bus":
                delta_P.append(0)
                delta_Q.append(0)
                continue

            P_calc, Q_calc = self.compute_power_injection(i, angles)
            dP = bus.P_spec - P_calc
            dQ = bus.Q_spec - Q_calc if bus.bus_type == "PQ Bus" else 0
            delta_P.append(dP)
            delta_Q.append(dQ)

        return np.array(delta_P), np.array(delta_Q)

    def print_power_mismatch(self, delta_P, delta_Q):
        print("\n--- Power Mismatch ---")
        for i, bus in enumerate(self.buses):
            print(f"{bus.name} ({bus.bus_type}):")
            print(f"  MW:   {delta_P[i]: .5f}")
            print(f"  MVAR: {delta_Q[i]: .5f}")

    def abc_to_seq(va, vb, vc):
        a = np.exp(1j * 2 * np.pi / 3)
        v0 = (va + vb + vc) / 3
        v1 = (va + a * vb + a**2 * vc) / 3
        v2 = (va + a**2 * vb + a * vc) / 3
        return v0, v1, v2

    def seq_to_abc(v0, v1, v2):
        a = np.exp(1j * 2 * np.pi / 3)
        va = v0 + v1 + v2
        vb = v0 + a**2 * v1 + a * v2
        vc = v0 + a * v1 + a**2 * v2
        return va, vb, vc


if __name__ == "__main__":
    from circuit_with_Solar_PV import Circuit
    from conductor import Conductor
    from bundle import Bundle
    from geometry import Geometry

    # Setup circuit
    circuit1 = Circuit("Circuit")

    # Add Buses
    circuit1.add_bus("Bus 1", 20, "Slack Bus")
    circuit1.add_bus("Bus 2", 230, "PQ Bus")
    circuit1.add_bus("Bus 3", 230, "PQ Bus")
    circuit1.add_bus("Bus 4", 230, "PQ Bus")
    circuit1.add_bus("Bus 5", 230, "PQ Bus")
    circuit1.add_bus("Bus 6", 230, "PQ Bus")
    circuit1.add_bus("Bus 7", 18, "PV Bus")

    # Add Transformers (now valid)
    circuit1.add_transformer("T1", "Bus 1", "Bus 2", 125, 8.5, 10, 100, "Yg-Yg", 0.0, 0.0)
    circuit1.add_transformer("T2", "Bus 6", "Bus 7", 200, 10.5, 12, 100, "Yg-Yg", 0.0, 0.0)

    # Add Line Properties
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

    # Add Loads
    circuit1.add_load("Load 3", "Bus 3", 110, 50)
    circuit1.add_load("Load 4", "Bus 4", 100, 70)
    circuit1.add_load("Load 5", "Bus 5", 100, 65)

    # Add Generators
    circuit1.add_generator("G1", "Bus 1", 1.0, 113.56)
    circuit1.add_generator("G2", "Bus 7", 1.0, 200)

    # Optionally add solar PV here (if needed for test)
    # circuit1.add_solar_pv(...)

    # Initialize and solve
    solution = SolutionSolarPV(buses=[], ybus=None, voltages=[])
    solution.initialize_system(circuit1)
    delta_P, delta_Q = solution.compute_power_mismatch_vector()
    solution.print_power_mismatch(delta_P, delta_Q)
