import numpy as np
from tabulate import tabulate
from solution import Solution
from jacobian import Jacobian

class PowerFlow:
    """
    ☀️ The PowerFlow class performs Newton-Raphson based power flow calculations.
    It utilizes mismatch calculations and Jacobian updates to iteratively solve bus voltages.
    """

    def __init__(self, solution: Solution, tol, max_iter):
        self.solution = solution
        self.buses = solution.buses
        self.ybus = solution.ybus
        self.tol = tol  # ☀️ Convergence tolerance
        self.max_iter = max_iter  # ☀️ Maximum number of iterations

    def calc_newton_raphson(self):
        """
        ☀️ Performs the Newton-Raphson iteration to solve for power flow.
        Returns True if converged, False otherwise.
        """
        for iteration in range(self.max_iter):
            pq_indices = [i for i, bus in enumerate(self.buses) if bus.bus_type == "PQ Bus"]
            pv_pq_indices = [i for i, bus in enumerate(self.buses) if bus.bus_type != "Slack Bus"]

            delta_P, delta_Q = self.solution.compute_power_mismatch_vector()
            delta_P_vector = delta_P[pv_pq_indices]
            delta_Q_vector = delta_Q[pq_indices]
            mismatch_vector = np.concatenate((delta_P_vector, delta_Q_vector))

            # ☀️ Convergence check
            if np.all(np.abs(mismatch_vector) < self.tol):
                print(f"\n☀️ Converged in {iteration + 1} iterations")
                print("\n--- Final Converged Bus Voltage and Angles ---")
                for bus in self.buses:
                    print(f"{bus.name:6s} | V = {bus.vpu:.5f} pu | δ = {bus.delta:.5f}°")
                return True

            # ☀️ Build and solve using Jacobian matrix
            angles = [bus.delta for bus in self.buses]
            voltages = [bus.vpu for bus in self.buses]
            jacobian = Jacobian(buses=self.buses, ybus=self.ybus, angles=angles, voltages=voltages)
            J = jacobian.calc_jacobian()

            delta_x = np.linalg.solve(J, mismatch_vector)

            # ☀️ Update voltage angles (δ) for non-slack buses
            delta_delta = delta_x[0:len(pv_pq_indices)]
            idx = 0
            for i, bus in enumerate(self.buses):
                if bus.bus_type == "Slack Bus":
                    continue
                bus.delta += np.degrees(delta_delta[idx])
                idx += 1

            # ☀️ Update voltage magnitudes (V) for PQ buses
            delta_v = delta_x[len(pv_pq_indices):]
            idx = 0
            for i, bus in enumerate(self.buses):
                if bus.bus_type == "PQ Bus":
                    bus.vpu += delta_v[idx]
                    idx += 1

            self.solution.voltages = [bus.vpu for bus in self.buses]

        print("\n❌ Did not converge within the max number of iterations")
        return False

    def print_matrix(self, matrix, title="Matrix"):
        """☀️ Utility to print matrix in a formatted table."""
        print(f"\n--- {title} ---")
        headers = [f"Col {i+1}" for i in range(matrix.shape[1])]
        table = [[f"Row {i+1}"] + list(np.round(row, 5)) for i, row in enumerate(matrix)]
        print(tabulate(table, headers=[""] + headers, tablefmt="grid"))

    def print_vector(self, vector, title="Vector"):
        """☀️ Utility to print vector with index and value."""
        print(f"\n--- {title} ---")
        table = [[f"Idx {i+1}", round(val, 5)] for i, val in enumerate(vector)]
        print(tabulate(table, headers=["Index", "Value"], tablefmt="grid"))
