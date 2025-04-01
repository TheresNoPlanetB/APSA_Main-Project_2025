import numpy as np

class Solution:
    def __init__(self, ybus, buses, angles):
        """
        Initializes the system settings class with Ybus, buses, and angles.
        :param ybus: system admittance matrix
        :param buses: list of buses in the system
        :param angles: list of voltage angles for each bus
        """
        self.ybus = ybus  # System admittance matrix
        self.buses = buses  # List of Bus objects
        self.angles = angles  # List of voltage angles

    def compute_power_injection(self, buses, voltages, angles, bus_k, voltage_k, angle_k):
        """
        Calculate real and reactive power injection.
        :param buses: list of Bus objects for power injection
        :param voltages: list of voltages of the system
        :param angles: list of voltage angles of the system
        :param bus_k: index of the bus for which power injection is calculated
        :param voltage_k: voltage of bus_k
        :param angle_k: angle of bus_k
        :return: real power (P_k_sum) and reactive power (Q_k_sum) injections
        """
        P_k_list = []
        Q_k_list = []

        for bus in buses:
            bus_index = bus.index  # Ensure the Bus class has an 'index' attribute
            voltage = voltages[bus_index]  # Get voltage for the bus
            angle = angles[bus_index]  # Get voltage angle of the bus

            # Extract row of Ybus for this bus
            ybus_row = self.ybus[bus_index, :]

            # Calculate real and reactive power injections
            P_k = voltage_k * voltage * np.abs(ybus_row[bus_k]) * np.cos(angle_k - angle - np.angle(ybus_row[bus_k]))
            Q_k = voltage_k * voltage * np.abs(ybus_row[bus_k]) * np.sin(angle_k - angle - np.angle(ybus_row[bus_k]))

            P_k_list.append(P_k)
            Q_k_list.append(Q_k)

        P_k_sum = sum(P_k_list)
        Q_k_sum = sum(Q_k_list)

        return P_k_sum, Q_k_sum


# Example validation
if __name__ == "__main__":
    # Example Ybus matrix (2x2 for simplicity)
    ybus = np.array([[10+5j, -5-2j], [-5-2j, 10+5j]])

    # Example buses list with indices
    class Bus:
        def __init__(self, index):
            self.index = index

    buses = [Bus(0), Bus(1)]

    # Example voltages and angles
    voltages = [1.0, 1.0]
    angles = [0.0, np.pi/4]  # Angles in radians

    # Create Solution object
    solution = Solution(ybus, buses, angles)

    # Compute power injection for bus 0
    P_k_sum, Q_k_sum = solution.compute_power_injection(buses, voltages, angles, 0, 1.0, 0.0)

    print(f"Real Power Injection (P_k_sum): {P_k_sum}")
    print(f"Reactive Power Injection (Q_k_sum): {Q_k_sum}")
