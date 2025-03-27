from circuit import Circuit
from conductor import Conductor
from bundle import Bundle
from geometry import Geometry
from tabulate import tabulate

# Create circuit
circuit1 = Circuit("Circuit")

# Add Buses
circuit1.add_bus("Bus1", 20,"Slack Bus")
circuit1.add_bus("Bus2", 230,"PQ Bus")
circuit1.add_bus("Bus3", 230,"PQ Bus")
circuit1.add_bus("Bus4", 230,"PQ Bus")
circuit1.add_bus("Bus5", 230,"PQ Bus")
circuit1.add_bus("Bus6", 230,"PQ Bus")
circuit1.add_bus("Bus7", 18,"PQ Bus")

# Add Transformers
circuit1.add_transformer("T1", "Bus1", "Bus2", 125, 8.5, 10, 100)
circuit1.add_transformer("T2", "Bus6", "Bus7", 200, 10.5, 12, 100)

# Add Transmission Line Parameters
conductor1 = Conductor("Partridge", 0.642, 0.0217, 0.385, 460)
bundle1 = Bundle("Bundle A", 2, 1.5, conductor1)
geometry1 = Geometry("Geometry 1", 0, 0, 19.5, 0, 39, 0)

# Add Transmission Lines
circuit1.add_transmission_line("Line 1", "Bus2", "Bus4", bundle1, geometry1, 10)
circuit1.add_transmission_line("Line 2", "Bus2", "Bus3", bundle1, geometry1, 25)
circuit1.add_transmission_line("Line 3", "Bus3", "Bus5", bundle1, geometry1, 20)
circuit1.add_transmission_line("Line 4", "Bus4", "Bus6", bundle1, geometry1, 20)
circuit1.add_transmission_line("Line 5", "Bus5", "Bus6", bundle1, geometry1, 10)
circuit1.add_transmission_line("Line 6", "Bus4", "Bus5", bundle1, geometry1, 35)


# Add Load
circuit1.add_load("Load 3", "Bus 3", 110, 50)
circuit1.add_load("Load 4", "Bus 4", 100, 70)
circuit1.add_load("Load 5", "Bus 5", 100, 65)

# Add Generator
circuit1.add_generator("G1", "Bus 1", 100, 1.0)
circuit1.add_generator("G2", "Bus 7", 200, 1.0)


# Print network summary
#print(circuit1.network_summary())

# Compute Ybus matrix
circuit1.calc_ybus()

# Retrieve Ybus Matrix
ybus_matrix = circuit1.get_ybus()

# Print 7 Bus Power System Ybus Matrix
def print_ybus_table(ybus_matrix):
    # Format matrix elements as "real + imag j"
    formatted_matrix = [
        [f"Bus {i+1}"] + [f"{elem.real:.2f}{elem.imag:+.2f}j" for elem in row]
        for i, row in enumerate(ybus_matrix)
    ]

    # Print 7 Bus Power System Ybus Matrix
    print("\nYbus Admittance Matrix:")
    headers = ["Bus"] + [f"Bus {i+1}" for i in range(len(ybus_matrix))]
    print(tabulate(formatted_matrix, headers=headers, tablefmt="grid"))

# Display 7 Bus Power System Ybus Matrix
print_ybus_table(ybus_matrix)