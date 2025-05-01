from circuit import Circuit
from bundle import Bundle
from geometry import Geometry
from solution import Solution
from jacobian import Jacobian
from powerflow import PowerFlow
from solarpv import SolarPV
import numpy as np
from conductor import Conductor

# Create the main circuit object for the full power system simulation
circuit1 = Circuit("Circuit")

# Add buses to the system (Slack, PQ, and PV bus types)
circuit1.add_bus("Bus 1", 20, "Slack Bus")
circuit1.add_bus("Bus 2", 230, "PQ Bus")
circuit1.add_bus("Bus 3", 230, "PQ Bus")
circuit1.add_bus("Bus 4", 230, "PQ Bus")
circuit1.add_bus("Bus 5", 230, "PQ Bus")
circuit1.add_bus("Bus 6", 230, "PQ Bus")
circuit1.add_bus("Bus 7", 18, "PV Bus")

# Add transformers connecting different voltage levels
circuit1.add_transformer("T1", "Bus 1", "Bus 2", 125, 8.5, 10, 100, connection_type="Y-Y", zg1=None, zg2=None)
circuit1.add_transformer("T2", "Bus 6", "Bus 7", 200, 10.5, 12, 100, connection_type="Y-Y", zg1=None, zg2=None)

# Define and add transmission lines
conductor1 = Conductor("Partridge", 0.642, 0.0217, 0.385, 460)
bundle1 = Bundle("Bundle A", 2, 1.5, conductor1)
geometry1 = Geometry("Geometry 1", 0, 0, 19.5, 0, 39, 0)

circuit1.add_transmission_line("Line 1", "Bus 2", "Bus 4", bundle1, geometry1, 10, connection_type="Transposed")
circuit1.add_transmission_line("Line 2", "Bus 2", "Bus 3", bundle1, geometry1, 25, connection_type="Transposed")
circuit1.add_transmission_line("Line 3", "Bus 3", "Bus 5", bundle1, geometry1, 20, connection_type="Transposed")
circuit1.add_transmission_line("Line 4", "Bus 4", "Bus 6", bundle1, geometry1, 20, connection_type="Transposed")
circuit1.add_transmission_line("Line 5", "Bus 5", "Bus 6", bundle1, geometry1, 10, connection_type="Transposed")
circuit1.add_transmission_line("Line 6", "Bus 4", "Bus 5", bundle1, geometry1, 35, connection_type="Transposed")

# Add loads at specific buses with real and reactive power values
circuit1.add_load("Load 3", "Bus 3", 110, 50)
circuit1.add_load("Load 4", "Bus 4", 100, 70)
circuit1.add_load("Load 5", "Bus 5", 100, 65)

# Add synchronous generators
circuit1.add_generator("G1", "Bus 1", 1.0, 100, 0.12, 0.14, 0.05, 125, grounded=False)
circuit1.add_generator("G2", "Bus 7", 1.0, 200, 0.12, 0.14, 0.05, 200, grounded=False)

# ✅ Add SolarPV unit (Test Case 1): 10 MW at 0.95 pu voltage on Bus 1
circuit1.add_solar_pv("PV4", "Bus 1", 10)

# Uncomment the following line to test 25 MW PV at Bus 1 with default 1.0 pu
# circuit1.add_solar_pv("PV5", "Bus 1", 25)

# 3. Validation Checks (Edge Testing):
# The following examples can be uncommented for error handling tests
# try:
#     circuit1.add_solar_pv("PV_BAD1", "Bus 3", -20)  # Invalid negative power
# except ValueError as e:
#     print("Caught error as expected (negative power):", e)
#
# try:
#     pv = SolarPV("PV_BAD2", circuit1.buses["Bus 4"], 20, voltage_setpoint=1.2)  # Invalid voltage
# except ValueError as e:
#     print("Caught error as expected (voltage out of range):", e)

# Print network summary to confirm all components
print(circuit1.network_summary())

# Compute Ybus matrix used for power flow analysis
circuit1.calc_ybus_powerflow()
circuit1.calc_ybus_faultstudy(sequence='positive')
circuit1.calc_zbus()

# Display the Ybus power flow matrix
print("PowerFlow Y bus")
circuit1.print_ybus_powerflow_table()

# Prepare and run the power flow solution using Newton-Raphson method
solution = Solution(buses=[], ybus=None, voltages=[])
solution.initialize_system(circuit1)

# Compute power mismatches before solving
delta_P, delta_Q = solution.compute_power_mismatch_vector()
solution.print_power_mismatch(delta_P, delta_Q)

# Form and print the Jacobian matrix
buses = solution.buses
ybus = solution.ybus
angles = [bus.delta for bus in buses]
voltages = [bus.vpu for bus in buses]
jacobian = Jacobian(buses=buses, ybus=ybus, angles=angles, voltages=voltages)
J = jacobian.calc_jacobian()
jacobian.print_jacobian(J)

# Solve the system using Newton-Raphson method
powerflow = PowerFlow(solution=solution, tol=0.001, max_iter=5)
powerflow.calc_newton_raphson()
solution.print_power_mismatch(*solution.compute_power_mismatch_vector())

# Print fault study matrices (positive, negative, zero sequences)
circuit1.print_ybus_faultstudy_table()
circuit1.print_zbus_table()

print("\n--- Sequence Impedance Matrices ---")
for seq in ['positive', 'negative', 'zero']:
    circuit1.calc_ybus_faultstudy(seq)
    print(f"\nY{seq[0].upper()} (Sequence Ybus):")
    circuit1.print_ybus_faultstudy_table()
    Z = np.linalg.inv(circuit1.get_ybus_faultstudy())
    print(f"\nZ{seq[0].upper()} (Sequence Zbus):")
    circuit1.zbus = Z
    circuit1.print_zbus_table()

# Run symmetrical and asymmetrical fault simulations at Bus 4
circuit1.run_sym_fault(4)
circuit1.run_asym_fault("SLG", 4)
circuit1.run_asym_fault("LL", 4)
circuit1.run_asym_fault("DLG", 4)
