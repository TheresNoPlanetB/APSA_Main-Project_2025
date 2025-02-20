from circuit import Circuit
from conductor import Conductor
from bundle import Bundle
from geometry import Geometry

# Create a circuit
circuit1 = Circuit("Circuit")

# Adding Buses
circuit1.add_bus("Bus1", 230)
circuit1.add_bus("Bus2", 230)
circuit1.add_bus("Bus3", 230)
circuit1.add_bus("Bus4", 230)
circuit1.add_bus("Bus5", 230)
circuit1.add_bus("Bus6", 230)
circuit1.add_bus("Bus7", 230)

# Adding Transformers
circuit1.add_transformer("T1", "Bus1", "Bus2", 125, 8.5, 10, 100, 34.64, 230)
circuit1.add_transformer("T2", "Bus6", "Bus7", 200, 10.5, 12, 100, 31.18, 230)

# Adding Transmission Lines
conductor1 = Conductor("Partridge", 0.642, 0.0217, 0.385, 460)
bundle1 = Bundle("Bundle A", 2, 1.5, conductor1)
geometry1 = Geometry("Geometry 1", 0, 0, 18.5, 0, 37, 0)

circuit1.add_transmission_line("Line 1", "Bus2", "Bus4", bundle1, geometry1, 10)
circuit1.add_transmission_line("Line 2", "Bus2", "Bus3", bundle1, geometry1, 25)
circuit1.add_transmission_line("Line 3", "Bus3", "Bus5", bundle1, geometry1, 20)
circuit1.add_transmission_line("Line 4", "Bus4", "Bus6", bundle1, geometry1, 20)
circuit1.add_transmission_line("Line 5", "Bus5", "Bus6", bundle1, geometry1, 10)
circuit1.add_transmission_line("Line 6", "Bus4", "Bus5", bundle1, geometry1, 35)

# Print network summary
print(circuit1.network_summary())

# Compute Ybus matrix
circuit1.calc_ybus()

# Retrieve and display Ybus
ybus_matrix = circuit1.get_ybus()

# Print the Ybus matrix
print("Ybus Matrix:")
for row in ybus_matrix:
    print(" ".join(f"{elem.real:.4f}{elem.imag:+.4f}j" for elem in row))
