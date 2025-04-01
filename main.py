import numpy as np

from circuit import Circuit
from conductor import Conductor
from bundle import Bundle
from geometry import Geometry
from solution import Solution

# Create circuit
circuit1 = Circuit("Circuit")

# Add Buses
circuit1.add_bus("Bus 1", 20,"Slack Bus")
circuit1.add_bus("Bus 2", 230,"PQ Bus")
circuit1.add_bus("Bus 3", 230,"PQ Bus")
circuit1.add_bus("Bus 4", 230,"PQ Bus")
circuit1.add_bus("Bus 5", 230,"PQ Bus")
circuit1.add_bus("Bus 6", 230,"PQ Bus")
circuit1.add_bus("Bus 7", 18,"PV Bus")

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
circuit1.add_load("Load 2", "Bus 2", 100, 70)
circuit1.add_load("Load 3", "Bus 3", 110, 50)
circuit1.add_load("Load 4", "Bus 4", 100, 70)
circuit1.add_load("Load 5", "Bus 5", 100, 65)
circuit1.add_load("Load 6", "Bus 6", 110, 50)

# Add Generator
circuit1.add_generator("G1", "Bus 1", 100, 1.0)
circuit1.add_generator("G2", "Bus 7", 200, 1.0)


# Print network summary
print(circuit1.network_summary())

# Compute Ybus matrix
circuit1.calc_ybus()

# Display 7 Bus Power System Ybus Matrix
circuit1.print_ybus_table()

#Define solution object
solution1 = Solution(circuit1.ybus, circuit1.buses)

#Create a vector y of initial real power and reactive power
#P2, P3, P4, P5, P6, P7, Q2, Q3, Q4, Q5, Q6
y = np.array([[100], [110], [100], [100], [110], [1], [70], [50], [70], [65], [50]])

print(f"Initial Vector y: {y}")

#Calculate Power injection
S_i_list, P_i_list, Q_i_list = solution1.compute_power_injection()

#print(f"S_i_list: {S_i_list}")
#print(f"P_i_list: {P_i_list}")
#print(f"Q_i_list: {Q_i_list}")


#Create a power injection array f of calculated real and reactive power

f = np.array([[P_i_list[0]],[P_i_list[1]],[P_i_list[2]], [P_i_list[3]],
              [P_i_list[4]], [P_i_list[5]],
              [Q_i_list[0]], [Q_i_list[1]], [Q_i_list[2]], [Q_i_list[3]],
              [Q_i_list[4]]
              ])
print(f"Power Injection Vector f: {f}")

#Create Subtraction to calculate power mismatch : 0 = y-f
power_mismatch = y - f

print(f"Power Mismatch Vector: {power_mismatch}")

