from circuit import Circuit
from conductor import Conductor
from bundle import Bundle
from geometry import Geometry
from solution import Solution
from jacobian import Jacobian
from powerflow import PowerFlow
import numpy as np


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
circuit1.add_transformer("T1", "Bus 1", "Bus 2", 125, 8.5, 10, 100, connection_type = "DELTA-WYE", zg1 = None, zg2 = 1.0)
circuit1.add_transformer("T2", "Bus 6", "Bus 7", 200, 10.5, 12, 100, connection_type = "WYE-DELTA", zg1 = None, zg2 = None)

# Add Transmission Line Parameters
conductor1 = Conductor("Partridge", 0.642, 0.0217, 0.385, 460)
bundle1 = Bundle("Bundle A", 2, 1.5, conductor1)
geometry1 = Geometry("Geometry 1", 0, 0, 19.5, 0, 39, 0)

# Add Transmission Lines
circuit1.add_transmission_line("Line 1", "Bus 2", "Bus 4", bundle1, geometry1, 10, connection_type = "Transposed")
circuit1.add_transmission_line("Line 2", "Bus 2", "Bus 3", bundle1, geometry1, 25, connection_type = "Transposed")
circuit1.add_transmission_line("Line 3", "Bus 3", "Bus 5", bundle1, geometry1, 20, connection_type = "Transposed")
circuit1.add_transmission_line("Line 4", "Bus 4", "Bus 6", bundle1, geometry1, 20, connection_type = "Transposed")
circuit1.add_transmission_line("Line 5", "Bus 5", "Bus 6", bundle1, geometry1, 10, connection_type = "Transposed")
circuit1.add_transmission_line("Line 6", "Bus 4", "Bus 5", bundle1, geometry1, 35, connection_type = "Transposed")

# Add Load
circuit1.add_load("Load 3", "Bus 3", 110, 50)
circuit1.add_load("Load 4", "Bus 4", 100, 70)
circuit1.add_load("Load 5", "Bus 5", 100, 65)

# Add Generator
circuit1.add_generator("G1", "Bus 1", 1.0, 100, 0.12, 0.14, 0.05, 125, grounded = True)
circuit1.add_generator("G2", "Bus 7", 1.0, 200, 0.12, 0.14, 0.05, 200, grounded = True)

# Print network summary
print(circuit1.network_summary())

# Compute Ybus matrix for power flow
circuit1.calc_ybus_powerflow()

# Compute Ybus matrix for fault study
circuit1.calc_ybus_faultstudy(sequence='positive')

# Compute Zbus matrix for fault study
circuit1.calc_zbus()

# Display 7 Bus Power System Ybus Power Flow Matrix
print("PowerFlow Y bus")
circuit1.print_ybus_powerflow_table()

# Power Mismatch
solution = Solution(buses=[], ybus=None, voltages=[])
solution.initialize_system(circuit1)
delta_P, delta_Q = solution.compute_power_mismatch_vector()
solution.print_power_mismatch(delta_P, delta_Q)

# Get bus and Ybus data
buses = solution.buses
ybus = solution.ybus
angles = [bus.delta for bus in buses]
voltages = [bus.vpu for bus in buses]

# Compute and print the Jacobian
jacobian = Jacobian(buses=buses, ybus=ybus, angles=angles, voltages=voltages)
J = jacobian.calc_jacobian()
jacobian.print_jacobian(J)

# Newton Raphson Power Flow
powerflow = PowerFlow(solution=solution, tol = 0.001, max_iter = 5)
powerflow.calc_newton_raphson()
solution.print_power_mismatch(*solution.compute_power_mismatch_vector())

# Display 7 Bus Power System Ybus Fault Study Matrix
circuit1.print_ybus_faultstudy_table()

# Display 7 Bus Power System Zbus
circuit1.print_zbus_table()

# Compute and print Y1, Z1, Y2, Z2, Y0, Z0 matrices
print("\n--- Sequence Impedance Matrices ---")

# Positive-sequence
circuit1.calc_ybus_faultstudy('positive')
print("\nY1 (Positive Sequence Ybus):")
circuit1.print_ybus_faultstudy_table()
Z1 = np.linalg.inv(circuit1.get_ybus_faultstudy())
print("\nZ1 (Positive Sequence Zbus):")
circuit1.zbus = Z1
circuit1.print_zbus_table()

# Negative-sequence
circuit1.calc_ybus_faultstudy('negative')
print("\nY2 (Negative Sequence Ybus):")
circuit1.print_ybus_faultstudy_table()
Z2 = np.linalg.inv(circuit1.get_ybus_faultstudy())
print("\nZ2 (Negative Sequence Zbus):")
circuit1.zbus = Z2
circuit1.print_zbus_table()

# Zero-sequence
circuit1.calc_ybus_faultstudy('zero')
print("\nY0 (Zero Sequence Ybus):")
circuit1.print_ybus_faultstudy_table()
Z0 = np.linalg.inv(circuit1.get_ybus_faultstudy())
print("\nZ0 (Zero Sequence Zbus):")
circuit1.zbus = Z0
circuit1.print_zbus_table()

# Run a Symmetrical (3-Phase) Fault at Bus 4
circuit1.run_sym_fault(4)  # Applies 3-phase fault at Bus 4

# Run a Single Line-to-Ground (SLG) Fault at Bus 4
circuit1.run_asym_fault("SLG", 4)  # Applies SLG fault at Bus 4

# Run a Line-to-Line (LL) Fault at Bus 4
circuit1.run_asym_fault("LL", 4)  # Applies LL fault at Bus 4

# Run a Double Line-to-Ground (DLG) Fault at Bus 4
circuit1.run_asym_fault("DLG", 4)  # Applies DLG fault at Bus 4
