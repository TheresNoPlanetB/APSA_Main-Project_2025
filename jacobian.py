import numpy as np
from tabulate import tabulate

class Jacobian:

    def __init__(self, buses, ybus, angles, voltages):
        self.buses = buses
        self.ybus = ybus
        self.angles = angles
        self.voltages = voltages

    def calc_jacobian(self):

        n = len(self.buses)
        angles = [bus.delta for bus in self.buses]
        V = self.voltages

        J11 = np.zeros((n, n))  # ∂P/∂δ
        J12 = np.zeros((n, n))  # ∂P/∂V
        J21 = np.zeros((n, n))  # ∂Q/∂δ
        J22 = np.zeros((n, n))  # ∂Q/∂V

        for i, bus_i in enumerate(self.buses):
            if bus_i.bus_type == "Slack Bus":
                continue

            V_i = V[i]
            delta_i = np.radians(angles[i])

            for j, bus_j in enumerate(self.buses):
                V_j = V[j]
                delta_j = np.radians(angles[j])
                Y_ij = self.ybus[i, j]
                G_ij = Y_ij.real
                B_ij = Y_ij.imag

                theta_ij = delta_i - delta_j

                if i == j:
                    for k, bus_k in enumerate(self.buses):
                        if k == i:
                            continue
                        V_k = V[k]
                        delta_k = np.radians(angles[k])
                        Y_ik = self.ybus[i, k]
                        G_ik = Y_ik.real
                        B_ik = Y_ik.imag

                        theta_ik = delta_i - delta_k

                        J11[i, i] += V_i * V_k * (G_ik * np.sin(theta_ik) - B_ik * np.cos(theta_ik))
                        J12[i, i] += V_k * (G_ik * np.cos(theta_ik) + B_ik * np.sin(theta_ik))
                        J21[i, i] += -V_i * V_k * (G_ik * np.cos(theta_ik) + B_ik * np.sin(theta_ik))
                        J22[i, i] += V_k * (G_ik * np.sin(theta_ik) - B_ik * np.cos(theta_ik))

                    J11[i, i] *= -1
                    J12[i, i] += 2 * V_i * self.ybus[i, i].real
                    J21[i, i] *= -1
                    J22[i, i] -= 2 * V_i * self.ybus[i, i].imag

                else:
                    J11[i, j] = -V_i * V_j * (-G_ij * np.sin(theta_ij) + B_ij * np.cos(theta_ij))
                    J12[i, j] = V_i * (G_ij * np.cos(theta_ij) + B_ij * np.sin(theta_ij))
                    J21[i, j] = -V_i * V_j * (G_ij * np.cos(theta_ij) + B_ij * np.sin(theta_ij))
                    J22[i, j] = V_i * (G_ij * np.sin(theta_ij) - B_ij * np.cos(theta_ij))

        # Filter buses: exclude slack from both rows/columns. PV exclude from Q rows/cols
        pq_pv_indices = [i for i, bus in enumerate(self.buses) if bus.bus_type in ("PQ Bus", "PV Bus")]
        pq_indices = [i for i, bus in enumerate(self.buses) if bus.bus_type == "PQ Bus"]

        J11_red = J11[np.ix_(pq_pv_indices, pq_pv_indices)]
        J12_red = J12[np.ix_(pq_pv_indices, pq_indices)]
        J21_red = J21[np.ix_(pq_indices, pq_pv_indices)]
        J22_red = J22[np.ix_(pq_indices, pq_indices)]

        # Combine the submatrices into full Jacobian
        J_top = np.hstack((J11_red, J12_red))
        J_bottom = np.hstack((J21_red, J22_red))
        J_full = np.vstack((J_top, J_bottom))

        return J_full

    def print_jacobian(self, J):
        num_rows, num_cols = J.shape
        row_labels = [f"Row {i + 1}" for i in range(num_rows)]
        col_labels = [f"Column {i + 1}" for i in range(num_cols)]

        # Combine labels and matrix into tabular data
        data_with_labels = [
            [row_labels[i]] + list(np.round(J[i], 4)) for i in range(num_rows)
        ]

        # Print formatted table
        print("\nJacobian Matrix:")
        print(tabulate(data_with_labels, headers=[""] + col_labels, tablefmt="grid"))

if __name__ == '__main__':
    from solution import Solution
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
    circuit1.add_generator("G1", "Bus 1", 1.0, 100)
    circuit1.add_generator("G2", "Bus 7", 1.0, 200)

    # Create and initialize solution
    solution = Solution(buses=[], ybus=None, voltages=[])
    solution.initialize_system(circuit1)

    # Get Buses and Ybus from the solution class
    buses = solution.buses
    ybus = solution.ybus

    # Power World Data
    angles = [bus.delta for bus in buses]
    voltages = [bus.vpu for bus in buses]

    # Create and compute Jacobian
    jacobian = Jacobian(buses=buses, ybus=ybus, angles = angles, voltages = voltages)
    J = jacobian.calc_jacobian()

    # Print Jacobian Matrix
    # After calculating the Jacobian matrix
    np.set_printoptions(precision=4, suppress=True)
    J = jacobian.calc_jacobian()

    jacobian.print_jacobian(J)