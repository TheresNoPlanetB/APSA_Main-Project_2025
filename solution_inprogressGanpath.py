import numpy as np

class Solution:
    def __init__(self, ybus, buses, angles):
        """
        Initializes the system settings class with Ybus and buses.
        :param ybus: system admittance matrix
        :param buses: list of buses in the system
        """
        self.ybus = ybus #System admittance matrix
        self.buses = buses # List of Bus objects

    def compute_power_injection(self, buses, voltages, angles, bus_k, voltage_k, angle_k):
        """
        Calculate real and reactive power injection.
        :param buses: buses list having buses object for power injection. buses = [bus_k, bus_n]
        :param voltages: voltage of system
        :P: Real power injection (W)
        :Q: Reactive power injection (VAR)
        """
        P_k_list = []
        Q_k_list = []
        i = 0
        while i < buses.size():
            bus_index = buses[i].index # Ensure the Bus class has an 'index' attribute
            voltage = voltages[bus_index] # Get voltage for the bus
            angle = angles[bus_index] #Get voltage angle of the bus

            # Extract row of Ybus for this bus
            ybus_row = self.ybus[bus_index, :]
            ybus_current = ybus_row[i]

        # Calculate complex power S_i
            #S_i = voltage * np.sum(ybus_row * np.conj(voltages)) # Complex power equation
            #Calculate Real Power
            P_k = voltage_k * voltage * ybus_current * np.cos(angle_k - angle - ybus.angle)
            P_k_list.append(P_k)

            #Calculate Reactive Power
            Q_k = voltage_k * voltage * ybus_current * np.sin(angle_k - angle - ybus.angle)
            Q_k_list.append(Q_k)

            i = i+1

            #P_i = np.real(S_i) # Real Power component
            #Q_i = np.imag(S_i) # Reactive Power component

        P_k_sum = sum(P_k_list)
        Q_k_sum = sum(Q_k_list)

        return P_k_sum, Q_k_sum

    #Investigate ybus_row calcuation
    #Investigate how to get y bus angle
    #Investiage how bus_k is fed into the program