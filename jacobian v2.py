import numpy as np
from bus import Bus


class Jacobian:
    def __init__(self, ybus, buses, voltages, angles):
        """
        Initializes the Jacobian class with Ybus, buses, voltages, and angles.
        :param ybus: system admittance matrix
        :param buses: list of buses in the system
        :param voltages: list of voltage magnitudes for each bus
        :param angles: list of voltage angles for each bus
        """
        self.ybus = ybus
        self.buses = buses
        self.voltages = voltages
        self.angles = angles

    def calc_jacobian(self):
        """
        Calculate the full Jacobian matrix.
        :return: Jacobian matrix J
        """
        J1 = self.calc_J1()
        J2 = self.calc_J2()
        J3 = self.calc_J3()
        J4 = self.calc_J4()

        # Construct the full Jacobian matrix
        J_top = np.hstack((J1, J2))
        J_bottom = np.hstack((J3, J4))
        J = np.vstack((J_top, J_bottom))

        return J

    def calc_J1(self):
        """
        Calculate the J1 (dP/dδ) submatrix of the Jacobian.
        :return: J1 matrix
        """
        J1 = np.zeros((len(self.buses), len(self.buses)))
        for i, bus_i in enumerate(self.buses):
            for j, bus_j in enumerate(self.buses):
                if i == j:
                    J1[i, j] = -self.voltages[i] * np.sum(
                        self.voltages * np.abs(self.ybus[i, :]) * np.sin(self.angles[i] - self.angles + np.angle(self.ybus[i, :]))
                    )
                else:
                    J1[i, j] = self.voltages[i] * self.voltages[j] * np.abs(self.ybus[i, j]) * np.sin(self.angles[i] - self.angles[j] + np.angle(self.ybus[i, j]))
        return J1

    def calc_J2(self):
        """
        Calculate the J2 (dP/dV) submatrix of the Jacobian.
        :return: J2 matrix
        """
        J2 = np.zeros((len(self.buses), len(self.buses)))
        for i, bus_i in enumerate(self.buses):
            for j, bus_j in enumerate(self.buses):
                if i == j:
                    J2[i, j] = self.voltages[i] * np.abs(self.ybus[i, i]) * np.cos(np.angle(self.ybus[i, i]))
                else:
                    J2[i, j] = self.voltages[i] * np.abs(self.ybus[i, j]) * np.cos(self.angles[i] - self.angles[j] + np.angle(self.ybus[i, j]))
        return J2

    def calc_J3(self):
        """
        Calculate the J3 (dQ/dδ) submatrix of the Jacobian.
        :return: J3 matrix
        """
        J3 = np.zeros((len(self.buses), len(self.buses)))
        for i, bus_i in enumerate(self.buses):
            for j, bus_j in enumerate(self.buses):
                if i == j:
                    J3[i, j] = self.voltages[i] * np.sum(
                        self.voltages * np.abs(self.ybus[i, :]) * np.cos(self.angles[i] - self.angles + np.angle(self.ybus[i, :]))
                    )
                else:
                    J3[i, j] = -self.voltages[i] * self.voltages[j] * np.abs(self.ybus[i, j]) * np.cos(self.angles[i] - self.angles[j] + np.angle(self.ybus[i, j]))
        return J3

    def calc_J4(self):
        """
        Calculate the J4 (dQ/dV) submatrix of the Jacobian.
        :return: J4 matrix
        """
        J4 = np.zeros((len(self.buses), len(self.buses)))
        for i, bus_i in enumerate(self.buses):
            for j, bus_j in enumerate(self.buses):
                if i == j:
                    J4[i, j] = -self.voltages[i] * np.abs(self.ybus[i, i]) * np.sin(np.angle(self.ybus[i, i]))
                else:
                    J4[i, j] = -self.voltages[i] * np.abs(self.ybus[i, j]) * np.sin(self.angles[i] - self.angles[j] + np.angle(self.ybus[i, j]))
        return J4

# Example validation
if __name__ == "__main__":
    # Example Ybus matrix (2x2 for simplicity)
    ybus = np.array([[10+5j, -5-2j], [-5-2j, 10+5j]])

    # Example buses list with indices
    class Bus:
        def __init__(self, index, P, Q):
            self.index = index
            self.P = P
            self.Q = Q

    buses = [Bus(0, 1.0, 0.5), Bus(1, 1.0, 0.5)]

    # Example voltages and angles
    voltages = [1.0, 1.0]
    angles = [0.0, np.pi/4]  # Angles in radians

    # Create Jacobian object
    jacobian = Jacobian(ybus, buses, voltages, angles)

    # Calculate the Jacobian matrix
    J = jacobian.calc_jacobian()

    print("Jacobian Matrix:")
    print(J)
