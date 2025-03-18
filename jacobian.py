import numpy as np

class Jacobian:
    def __init__(self, buses, ybus, angles, voltages):
        """
        Initializes the Jacobian object with buses, Ybus matrix, voltage angles and magnitudes.

        """
        self.buses = buses #List of Bus objects
        self.ybus = ybus  #Admittance matrix of the system (Ybus)
        self.angles = angles # Voltage angles of buses
        self.voltages = voltages # Voltage magnitudes of buses
        self.J = None  # Will store the full Jacobian matrix

    def calc_jacobian(self):
        """
        Calculates the Jacobian matrix by computing each sub-matrix: J1, J2, J3, J4.
        """
        # Number of buses excluding the slack bus
        n = len(self.buses) - 1

        # Initialize the four sub-matrices: J1, J2, J3, J4
        J1 = np.zeros((n, n))
        J2 = np.zeros((n, n))
        J3 = np.zeros((n, n))
        J4 = np.zeros((n, n))

        for i in range(n):
            for j in range(n):
                if i != j:  # Skip diagonal terms for simplicity
                    # Compute elements for J1, J2, J3, J4
                    J1[i, j] = self.dP_dDelta(i, j)
                    J2[i, j] = self.dP_dV(i, j)
                    J3[i, j] = self.dQ_dDelta(i, j)
                    J4[i, j] = self.dQ_dV(i, j)
                else:
                    # Diagonal terms are handled differently
                    J1[i, i] = self.dP_dDelta(i, i)
                    J2[i, i] = self.dP_dV(i, i)
                    J3[i, i] = self.dQ_dDelta(i, i)
                    J4[i, i] = self.dQ_dV(i, i)

        # Combine J1, J2, J3, J4 into the full Jacobian matrix
        self.J = np.block([
            [J1, J2],
            [J3, J4]
        ])

        return self.J

    def dP_dDelta(self, i, j):
        """
        Computes the partial derivative of real power with respect to the voltage angle (dP/dδ).
        """
        # Use Ybus matrix and current angles to compute the derivative
        # Formula: dP/dδ = Im(Y_ij * V_i * V_j *)
        V_i = self.voltages[i]
        V_j = self.voltages[j]
        angle_diff = self.angles[i] - self.angles[j]
        y_ij = self.ybus[i, j]  # Admittance of the connection between bus i and bus j

        return np.imag(y_ij * V_i * V_j * np.exp(-1j * angle_diff))

    def dP_dV(self, i, j):
        """
        Computes the partial derivative of real power with respect to the voltage magnitude (dP/dV).
        """
        # Use Ybus matrix and current voltages to compute the derivative
        V_i = self.voltages[i]
        V_j = self.voltages[j]
        y_ij = self.ybus[i, j]

        return np.real(y_ij * np.conj(V_j))

    def dQ_dDelta(self, i, j):
        """
        Computes the partial derivative of reactive power with respect to the voltage angle (dQ/dδ).
        """
        # Formula: dQ/dδ = Re(Y_ij * V_i * V_j *)
        V_i = self.voltages[i]
        V_j = self.voltages[j]
        angle_diff = self.angles[i] - self.angles[j]
        y_ij = self.ybus[i, j]

        return np.real(y_ij * V_i * V_j * np.exp(-1j * angle_diff))

    def dQ_dV(self, i, j):
        """
        Computes the partial derivative of reactive power with respect to the voltage magnitude (dQ/dV).
        """
        # Use Ybus matrix and current voltages to compute the derivative
        V_i = self.voltages[i]
        V_j = self.voltages[j]
        y_ij = self.ybus[i, j]

        return -np.imag(y_ij * np.conj(V_j))
