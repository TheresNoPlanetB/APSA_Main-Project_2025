from circuit import Circuit
from conductor import Conductor
from bundle import Bundle
from geometry import Geometry

# Create a circuit
circuit1 = Circuit("Circuit")

# Adding Buses
circuit1.add_bus("Bus1", 230)
circuit1.add_bus("Bus2", 230)

# Adding Transformers
circuit1.add_transformer("T1", "Bus1", "Bus2", 100, 8, 10, 100)

# Adding Transmission Lines
conductor1 = Conductor("Conductor A", 0.642, 0.0217, 0.385, 460)
bundle1 = Bundle("Bundle A", 2, 1.5, conductor1)
geometry1 = Geometry("Geometry 1", 5, 10, 18.5, 15, 37, 20)

circuit1.add_transmission_line("Line 1", "Bus1", "Bus2", bundle1, geometry1, 10)

# Print network summary
print(circuit1.network_summary())

"""
# Compute Ybus matrix
print("Computing Ybus Matrix...")
circuit1.calc_ybus()

# Retrieve and display the computed Ybus
ybus_matrix = circuit1.get_ybus()
print("Ybus Matrix:")
print(ybus_matrix)
"""