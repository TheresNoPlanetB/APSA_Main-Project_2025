import numpy as np

class Solution:
    def __init__(self, ybus, buses):
        """
        Initializes the system settings class with Ybus and buses.
        :param ybus: system admittance matrix
        :param buses: list of buses in the system
        """
        self.ybus = ybus #System admittance matrix
        self.buses = buses # List of Bus objects
        self.voltages = []
        self.S_i = []
        self.P_i = []
        self.Q_i = []
        self.S_i_list = []
        self.P_i_list = []
        self.Q_i_list = []


    def compute_power_injection(self):
        """
        Calculate real and reactive power injection.
        :param bus: specific bus for power injection
        :param voltages: voltage of system
        :P: Real power injection (W)
        :Q: Reactive power injection (VAR)
        """
        for key, value in self.buses.items():
            self.voltages.append(value.base_kv)
            #print(value.base_kv)

        for i in range(0, len(self.buses)):
            #skip slack bus
            if i != 1:
                voltage = self.voltages[i] # Get voltage for the bus
                ybus_row = self.ybus[i, :]

                # Calculate complex power S_i
                S_i_temp = voltage * np.conj(np.sum(ybus_row) + voltage) # Complex power equation
                self.S_i.append(S_i_temp)
                self.P_i.append(np.real(S_i_temp)) # Real Power component
                self.Q_i.append(np.imag(S_i_temp)) # Reactive Power component

        #Remove Q7 due to Generator Bus 7 not having reactive power

        Q7 = self.Q_i.pop()

        return self.S_i, self.P_i, self.Q_i
