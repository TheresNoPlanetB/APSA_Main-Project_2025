import numpy as np
from circuit import Circuit
import pandas as pd


class Solution:
    def __init__(self, ybus, buses):
        """
        Initializes the system settings class with Ybus and buses.
        :param ybus: system admittance matrix
        :param buses: list of buses in the system
        """
        self.ybus = ybus #System admittance matrix
        self.buses = buses # List of Bus objects

    def compute_power_injection(self, bus, voltages):
        """
        Calculate real and reactive power injection.
        :param bus: specific bus for power injection
        :param voltages: voltage of system
        :P: Real power injection (W)
        :Q: Reactive power injection (VAR)
        """
        bus_index = bus.index # Ensure the Bus class has an 'index' attribute
        voltage = voltages[bus_index] # Get voltage for the bus

        # Extract row of Ybus for this bus
        ybus_row = self.ybus[bus_index, :]

        # Calculate complex power S_i
        S_i = voltage * np.sum(ybus_row * np.conj(voltages)) # Complex power equation
        P_i = np.real(S_i) # Real Power component
        Q_i = np.imag(S_i) # Reactive Power component

        return P_i, Q_i