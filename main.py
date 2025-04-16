from circuit import Circuit
from conductor import Conductor
from bundle import Bundle
from geometry import Geometry
from solution import Solution
from jacobian import Jacobian
from powerflow import PowerFlow

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
circuit1.add_load("Load 3", "Bus 3", 110, 50)
circuit1.add_load("Load 4", "Bus 4", 100, 70)
circuit1.add_load("Load 5", "Bus 5", 100, 65)

# Add Generator
circuit1.add_generator("G1", "Bus 1", 1.0, 100, 0.12)
circuit1.add_generator("G2", "Bus 7", 1.0, 200, 0.12)

# Print network summary
print(circuit1.network_summary())

# Compute Ybus matrix for power flow
circuit1.calc_ybus_powerflow()

# Compute Ybus matrix for fault study
circuit1.calc_ybus_faultstudy()

# Compute Zbus matrix for fault study
circuit1.calc_zbus()

# Compute fault current
circuit1.calc_fault_current("Bus 1")

# Compute fault voltage
circuit1.calc_fault_bus_voltage("Bus 1", "Bus 2")

# Display 7 Bus Power System Ybus Power Flow Matrix
print("PowerFlow Y bus")
circuit1.print_ybus_powerflow_table()

# Display 7 Bus Power System Ybus Fault Study Matrix
print("FaultStudy Y bus")
circuit1.print_ybus_faultstudy_table()

# Display 7 Bus Power System Zbus
print("FaultStudy Y bus")
circuit1.print_zbus_table()

# Display 7 Bus Power System Zbus
print("Fault Current")
circuit1.print_fault_current("Bus 1")

# Display 7 Bus Power System Zbus
print("Fault Bus Voltage")
circuit1.print_fault_bus_voltage("Bus 1", "Bus 2")



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