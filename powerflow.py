import numpy as np
from solution import Solution
from jacobian import Jacobian

class PowerFlow:

    def __init__(self, solution: Solution, tol = 0.001, max_iter = 50):
        self.solution = solution
        self.buses = solution.buses
        self.ybus = solution.ybus
        self.tol = tol
        self.max_iter = max_iter

    def calc_newton_raphson(self):

        for iteration in range(self.max_iter):
            pq_indices = [i for i, bus in enumerate(self.buses) if bus.bus_type == "PQ Bus"]
            pv_pq_indices = [i for i, bus in enumerate(self.buses) if bus.bus_type != "Slack Bus"]

            delta_P, delta_Q = self.solution.compute_power_mismatch_vector()

            delta_P_vector = delta_P[pv_pq_indices]
            delta_Q_vector = delta_Q[pq_indices]

            mismatch_vector = np.concatenate((delta_P_vector, delta_Q_vector))

            # Power Mismatch Structure
            print(f"\nIteration {iteration}")
            print("Power Mismatch Shape", mismatch_vector.shape)
            print("Mismatch Vector (ΔP and ΔQ):")
            print(np.round(mismatch_vector, 4))

            if np.all(np.abs(mismatch_vector) < self.tol):
                print(f"\nConverged in {iteration} iterations")
                return

            angles = [bus.delta for bus in self.buses]
            voltages = [bus.vpu for bus in self.buses]
            jacobian = Jacobian(buses = self.buses, ybus = self.ybus, angles = angles, voltages = voltages)
            J = jacobian.calc_jacobian()

            # Jacobian Matrix
            print("Jacobian Matrix Shape", J.shape)
            print("Jacobian Matrix")
            print(np.round(J[:11, :11], 4))  # or use tabulate if needed

            delta_x = np.linalg.solve(J, mismatch_vector)

            idx = 0

            for i, bus in enumerate(self.buses):
                if bus.bus_type == "Slack Bus":
                    continue
                bus.delta += delta_x[idx]
                idx += 1
                if bus.bus_type == "PQ Bus":
                    bus.vpu += delta_x[idx]
                    bus.vpu = max(0.9, min(bus.vpu, 1.1))
                    idx += 1

            self.solution.voltages = [bus.vpu for bus in self.buses]

        print("\n Did not converge within the max number of iterations")