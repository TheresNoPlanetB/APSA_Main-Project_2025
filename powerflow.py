import numpy as np
from tabulate import tabulate
from solution import Solution
from jacobian import Jacobian

class PowerFlow:

    # Initializes th
    def __init__(self, solution: Solution, tol, max_iter):
        self.solution = solution
        self.buses = solution.buses
        self.ybus = solution.ybus
        self.tol = tol
        self.max_iter = max_iter

    def calc_newton_raphson(self):
        #print("\n--- Iteration 0 ---")
        #print("Initial Bus Voltages and Angles")

        # Loops through each bus and prints voltage pu and angle before iteration starts
        #for bus in self.buses:
            #print(f"{bus.name:.6s} | V = {bus.vpu:.5f} pu | δ = {bus.delta:.5f}°")

        # Runs the newton raphson iteration
        for iteration in range(self.max_iter):
            pq_indices = [i for i, bus in enumerate(self.buses) if bus.bus_type == "PQ Bus"] # PQ buses need both P and Q updated
            pv_pq_indices = [i for i, bus in enumerate(self.buses) if bus.bus_type != "Slack Bus"] # PV buses need P updated

            # Compute power mismatch
            delta_P, delta_Q = self.solution.compute_power_mismatch_vector()
            delta_P_vector = delta_P[pv_pq_indices]
            delta_Q_vector = delta_Q[pq_indices]
            mismatch_vector = np.concatenate((delta_P_vector, delta_Q_vector))

            # Check for convergence
            if np.all(np.abs(mismatch_vector) < self.tol):
                print(f"\nConverged in {iteration + 1} iterations")
                print("\n--- Final Converged Bus Voltage and Angles ---")
                for bus in self.buses:
                    print(f"{bus.name:6s} | V = {bus.vpu:.5f} pu | δ = {bus.delta:.5f}°")
                return True

            # Build jacobian matrix
            angles = [bus.delta for bus in self.buses]
            voltages = [bus.vpu for bus in self.buses]
            jacobian = Jacobian(buses = self.buses, ybus = self.ybus, angles = angles, voltages = voltages)
            J = jacobian.calc_jacobian()

            # Solves delta(x) = (J^-1) * mismatch_vector
            #self.print_vector(mismatch_vector, "Mismatch Vector [ΔP | ΔQ]")
            #self.print_matrix(J, "Jacobian Matrix J")
            delta_x = np.linalg.solve(J, mismatch_vector)
            #self.print_vector(delta_x, "Update Vector Δx")

            # Split update vectors
            delta_delta = delta_x[0:len(pv_pq_indices)]
            delta_v = delta_x[len(pv_pq_indices):]

            # Iterates through buses to update voltage pu and angle
            idx = 0
            for i, bus in enumerate(self.buses):
                if bus.bus_type == "Slack Bus":
                    continue
                bus.delta += np.degrees(delta_delta[idx])
                idx += 1

            idx = 0
            for i, bus in enumerate(self.buses):
                if bus.bus_type == "PQ Bus":
                    bus.vpu += delta_v[idx]
                    idx += 1

            # Saves the update votage pu
            self.solution.voltages = [bus.vpu for bus in self.buses]

            """
            # Prints iteration results and each iteration
            print(f"\n--- Iteration {iteration + 1} ---")
            for bus in self.buses:
                print(f"{bus.name:6s} | V = {bus.vpu:.5f} pu | δ = {bus.delta:.5f}°")

            # Print angle and voltage updates
            print("Updated Voltage Angles (deg):", [round(float(bus.delta), 4) for bus in self.buses])
            print("Updated Voltage Magnitudes (p.u.):", [round(float(bus.vpu), 4) for bus in self.buses])
            """

        print("\nDid not converge within the max number of iterations")
        return False

    def print_matrix(self, matrix, title="Matrix"):
        print(f"\n--- {title} ---")
        headers = [f"Col {i+1}" for i in range(matrix.shape[1])]
        table = [[f"Row {i+1}"] + list(np.round(row, 5)) for i, row in enumerate(matrix)]
        print(tabulate(table, headers=[""] + headers, tablefmt="grid"))

    def print_vector(self, vector, title="Vector"):
        print(f"\n--- {title} ---")
        table = [[f"Idx {i+1}", round(val, 5)] for i, val in enumerate(vector)]
        print(tabulate(table, headers=["Index", "Value"], tablefmt="grid"))